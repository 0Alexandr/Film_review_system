from django.test import TestCase
from django.urls import reverse


class CatalogTests(TestCase):
    def test_movie_list_opens(self) -> None:
        response = self.client.get(reverse("movie_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Интерстеллар")

    def test_movie_detail_opens(self) -> None:
        response = self.client.get(reverse("movie_detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Кристофер Нолан")

    def test_missing_movie_returns_404(self) -> None:
        response = self.client.get(reverse("movie_detail", args=[999]))

        self.assertEqual(response.status_code, 404)
