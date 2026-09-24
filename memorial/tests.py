from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings

from memorial.admin_auth import safe_admin_redirect_target
from memorial.content_data import (
    GALLERY_ROTATE_SESSION_KEY,
    _session_non_negative_int,
    get_home_page_content,
)
from memorial.models import HomePageContent


@override_settings(ALLOWED_HOSTS=["example.com"])
class SafeAdminRedirectTests(SimpleTestCase):
    def test_blocks_protocol_relative_open_redirect(self):
        request = RequestFactory().get("/dashboard/login/")
        request.META["HTTP_HOST"] = "example.com"
        self.assertIsNone(safe_admin_redirect_target("//evil.com/phish", request))

    def test_allows_same_site_path(self):
        request = RequestFactory().get("/dashboard/login/")
        request.META["HTTP_HOST"] = "example.com"
        self.assertEqual(
            safe_admin_redirect_target("/dashboard/gallery/", request),
            "/dashboard/gallery/",
        )


class GallerySessionOffsetTests(SimpleTestCase):
    def test_corrupt_session_value_falls_back_to_zero(self):
        session = {GALLERY_ROTATE_SESSION_KEY: "not-a-number"}
        self.assertEqual(_session_non_negative_int(session, GALLERY_ROTATE_SESSION_KEY), 0)

    def test_negative_session_value_clamps_to_zero(self):
        session = {GALLERY_ROTATE_SESSION_KEY: -3}
        self.assertEqual(_session_non_negative_int(session, GALLERY_ROTATE_SESSION_KEY), 0)


class HomePageContentTests(TestCase):
    def test_get_home_page_content_creates_single_row(self):
        self.assertEqual(HomePageContent.objects.count(), 0)
        first = get_home_page_content()
        second = get_home_page_content()
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(HomePageContent.objects.count(), 1)
