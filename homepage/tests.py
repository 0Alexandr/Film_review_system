from django.test import TestCase
from django.urls import reverse


class HomepageTests(TestCase):
    def test_homepage_opens(self) -> None:
        response = self.client.get(reverse("homepage:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/navigation.html")
        self.assertContains(response, "КиноОтзыв")
        self.assertIn("statistics", response.context)

    def test_static_files_are_linked(self) -> None:
        response = self.client.get(reverse("homepage:index"))

        self.assertContains(response, "homepage/css/style.css")
        self.assertContains(response, "homepage/js/main.js")
        self.assertContains(response, "homepage/img/logo.svg")

    def test_custom_404_returns_not_found(self) -> None:
        response = self.client.get("/unknown-page/")

        self.assertEqual(response.status_code, 404)
