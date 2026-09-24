import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.test import Client
from django.test.utils import override_settings

from memorial.content_data import (
    DEFAULT_HOME_PAGE,
    ensure_visit_locations,
    get_home_page_content,
    get_visit_destinations,
    seed_default_life_chapters,
)
from memorial.models import HomePageContent


class Command(BaseCommand):
    help = "Stress-test public pages in-process (parallel GETs, latency percentiles)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--workers",
            type=int,
            default=32,
            help="Concurrent worker threads (default: 32)",
        )
        parser.add_argument(
            "--requests",
            type=int,
            default=400,
            help="Total requests per path (default: 400)",
        )
        parser.add_argument(
            "--max-error-rate",
            type=float,
            default=0.01,
            help="Fail if error rate exceeds this fraction (default: 0.01)",
        )
        parser.add_argument(
            "--max-p95-ms",
            type=float,
            default=2500.0,
            help="Fail if p95 latency exceeds this many ms (default: 2500)",
        )

    def handle(self, *args, **options):
        workers = options["workers"]
        total = options["requests"]
        max_error_rate = options["max_error_rate"]
        max_p95_ms = options["max_p95_ms"]

        allowed_hosts = list(settings.ALLOWED_HOSTS)
        if "testserver" not in allowed_hosts:
            allowed_hosts.append("testserver")

        stress_caches = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "memorial-stress",
            }
        }
        with override_settings(ALLOWED_HOSTS=allowed_hosts, CACHES=stress_caches):
            self._warm_content()

            paths = [
                "/",
                "/gallery/",
                "/life-story/",
                "/tributes/",
                "/visit/",
                "/health/",
            ]
            overall_errors = 0
            overall_total = 0
            failed = False

            for path in paths:
                stats = self._run_path(path, workers, total)
                overall_errors += stats["errors"]
                overall_total += stats["total"]
                self.stdout.write(
                    f"{path}: ok={stats['ok']}/{stats['total']} "
                    f"p50={stats['p50']:.0f}ms p95={stats['p95']:.0f}ms max={stats['max']:.0f}ms"
                )
                if stats["error_rate"] > max_error_rate:
                    self.stderr.write(
                        self.style.ERROR(
                            f"  error rate {stats['error_rate']:.2%} > {max_error_rate:.2%}"
                        )
                    )
                    failed = True
                if stats["p95"] > max_p95_ms:
                    self.stderr.write(
                        self.style.ERROR(
                            f"  p95 {stats['p95']:.0f}ms > {max_p95_ms:.0f}ms"
                        )
                    )
                    failed = True

            error_rate = overall_errors / overall_total if overall_total else 0
            summary = (
                f"Overall: {overall_total - overall_errors}/{overall_total} OK "
                f"({error_rate:.2%} errors)"
            )
            if failed:
                self.stdout.write(self.style.WARNING(summary + " — thresholds exceeded"))
                raise SystemExit(1)
            self.stdout.write(self.style.SUCCESS(summary))

    def _warm_content(self):
        cache.clear()
        if not HomePageContent.objects.exists():
            HomePageContent.objects.create(**DEFAULT_HOME_PAGE)
        get_home_page_content()
        seed_default_life_chapters()
        ensure_visit_locations()
        get_visit_destinations()
        client = Client()
        for path in ("/", "/gallery/", "/life-story/", "/tributes/", "/visit/"):
            client.get(path)

    def _run_path(self, path, workers, total):
        latencies = []
        errors = 0

        def fetch():
            client = Client()
            start = time.perf_counter()
            try:
                response = client.get(path)
                elapsed_ms = (time.perf_counter() - start) * 1000
                return response.status_code, elapsed_ms
            except Exception:
                elapsed_ms = (time.perf_counter() - start) * 1000
                return 0, elapsed_ms

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(fetch) for _ in range(total)]
            for future in as_completed(futures):
                status, elapsed_ms = future.result()
                latencies.append(elapsed_ms)
                if status != 200:
                    errors += 1

        latencies.sort()
        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95) - 1] if latencies else 0
        return {
            "total": total,
            "ok": total - errors,
            "errors": errors,
            "error_rate": errors / total if total else 0,
            "p50": p50,
            "p95": p95,
            "max": max(latencies) if latencies else 0,
        }
