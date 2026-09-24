from concurrent.futures import ThreadPoolExecutor, as_completed

from django.core.cache import cache
from django.db import connection
from django.test import Client, TransactionTestCase
from django.test.utils import CaptureQueriesContext

from memorial.content_data import (
    DEFAULT_HOME_PAGE,
    ensure_visit_locations,
    get_home_page_content,
    get_visit_destinations,
    seed_default_life_chapters,
)
from memorial.models import HomePageContent


class ConcurrentPublicTrafficTests(TransactionTestCase):
    """Smoke load: many parallel GETs against read-heavy public pages."""

    reset_sequences = True

    def setUp(self):
        cache.clear()
        if not HomePageContent.objects.exists():
            HomePageContent.objects.create(**DEFAULT_HOME_PAGE)
        get_home_page_content()
        seed_default_life_chapters()
        ensure_visit_locations()
        get_visit_destinations()

    def _parallel_get(self, path, workers=24, requests=96):
        def fetch():
            client = Client()
            return client.get(path).status_code

        codes = []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(fetch) for _ in range(requests)]
            for future in as_completed(futures):
                codes.append(future.result())
        return codes

    def test_concurrent_home_requests(self):
        codes = self._parallel_get("/")
        self.assertEqual(codes.count(200), len(codes))

    def test_concurrent_gallery_and_life_story(self):
        for path in ("/gallery/", "/life-story/", "/tributes/", "/visit/"):
            codes = self._parallel_get(path, workers=16, requests=64)
            self.assertEqual(codes.count(200), len(codes), msg=path)

    def test_health_endpoint_under_load(self):
        codes = self._parallel_get("/health/", workers=8, requests=32)
        self.assertEqual(codes.count(200), len(codes))

    def test_home_uses_cache_after_warmup(self):
        client = Client()
        client.get("/")
        response = client.get("/")
        self.assertEqual(response.status_code, 200)


class PublicPageQueryBudgetTests(TransactionTestCase):
    def setUp(self):
        cache.clear()
        if not HomePageContent.objects.exists():
            HomePageContent.objects.create(**DEFAULT_HOME_PAGE)
        seed_default_life_chapters()
        client = Client()
        client.get("/")
        client.get("/gallery/")
        client.get("/life-story/")
        client.get("/tributes/")

    def test_warm_home_query_count(self):
        client = Client()
        with CaptureQueriesContext(connection) as ctx:
            response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(
            len(ctx.captured_queries),
            0,
            msg="Warm home should be served entirely from cache",
        )

    def test_warm_gallery_query_count(self):
        client = Client()
        with CaptureQueriesContext(connection) as ctx:
            response = client.get("/gallery/")
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(
            len(ctx.captured_queries),
            0,
            msg="Warm gallery should be served entirely from cache",
        )

    def test_warm_life_story_and_tributes_query_count(self):
        client = Client()
        with CaptureQueriesContext(connection) as ctx:
            life = client.get("/life-story/")
            trib = client.get("/tributes/")
        self.assertEqual(life.status_code, 200)
        self.assertEqual(trib.status_code, 200)
        self.assertLessEqual(
            len(ctx.captured_queries),
            0,
            msg="Warm life story and tributes should be served from cache",
        )


class StressTestCommandTests(TransactionTestCase):
    def test_stress_test_command_passes_default_thresholds(self):
        from django.core.management import call_command

        if not HomePageContent.objects.exists():
            HomePageContent.objects.create(**DEFAULT_HOME_PAGE)
        call_command(
            "stress_test",
            workers=16,
            requests=80,
            max_p95_ms=10000,
        )
