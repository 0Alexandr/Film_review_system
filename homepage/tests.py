from django.urls import reverse

from db.testing import TemporaryDatabaseTestCase


class HomepageTests(TemporaryDatabaseTestCase):
    def test_homepage_opens(self) -> None:
        response = self.client.get(reverse("homepage:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/navigation.html")
        self.assertContains(response, "КиноОтзыв")

    def test_homepage_uses_sqlite_data(self) -> None:
        response = self.client.get(reverse("homepage:index"))

        self.assertEqual(response.context["statistics"]["movies_count"], 5)
        self.assertEqual(len(response.context["top_movies"]), 3)
        self.assertEqual(
            response.context["top_movies"][0]["title"],
            "Интерстеллар",
        )
        self.assertEqual(len(response.context["latest_reviews"]), 5)

    def test_static_files_are_linked(self) -> None:
        response = self.client.get(reverse("homepage:index"))

        self.assertContains(response, "homepage/css/style.css")
        self.assertContains(response, "homepage/js/main.js")
        self.assertContains(response, "homepage/img/logo.svg")

    def test_custom_404_returns_not_found(self) -> None:
        response = self.client.get("/unknown-page/")

        self.assertEqual(response.status_code, 404)
