from django.test import TestCase
from django.urls import reverse


class HomepageTests(TestCase):
    def test_homepage_opens(self) -> None:
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "КиноОтзыв")

    def test_custom_404_returns_not_found(self) -> None:
        response = self.client.get("/unknown-page/")

        self.assertEqual(response.status_code, 404)
