from django.test import TestCase
from django.urls import reverse


class CatalogTests(TestCase):
    def test_movie_list_opens(self) -> None:
        response = self.client.get(reverse("catalog:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/movie_list.html")
        self.assertTemplateUsed(response, "catalog/includes/movie_card.html")
        self.assertContains(response, "Интерстеллар")
        self.assertContains(response, "Всего фильмов: 3")

    def test_movie_detail_opens(self) -> None:
        response = self.client.get(reverse("catalog:detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/movie_detail.html")
        self.assertContains(response, "Кристофер Нолан")

    def test_missing_movie_returns_404(self) -> None:
        response = self.client.get(reverse("catalog:detail", args=[999]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Фильм не найден", status_code=404)
