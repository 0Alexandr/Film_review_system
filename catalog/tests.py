from django.urls import reverse

from db.testing import TemporaryDatabaseTestCase


class CatalogTests(TemporaryDatabaseTestCase):
    def test_movie_list_opens(self) -> None:
        response = self.client.get(reverse("catalog:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/movie_list.html")
        self.assertTemplateUsed(response, "catalog/includes/movie_card.html")
        self.assertContains(response, "Интерстеллар")
        self.assertContains(response, "Всего фильмов: 5")

    def test_movie_without_reviews_is_listed(self) -> None:
        response = self.client.get(reverse("catalog:list"))

        self.assertContains(response, "Джокер")
        self.assertContains(response, "Оценок пока нет")

    def test_movie_detail_opens(self) -> None:
        response = self.client.get(reverse("catalog:detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/movie_detail.html")
        self.assertContains(response, "Кристофер Нолан")
        self.assertEqual(len(response.context["reviews"]), 2)

    def test_missing_movie_returns_404(self) -> None:
        response = self.client.get(reverse("catalog:detail", args=[999]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Фильм не найден", status_code=404)

    def test_search_form_without_parameters(self) -> None:
        response = self.client.get(reverse("catalog:search"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/movie_search.html")
        self.assertContains(response, "Задайте условия")

    def test_search_by_genre_and_rating(self) -> None:
        response = self.client.get(
            reverse("catalog:search"),
            {"genre": "Фантастика", "min_rating": "8"},
        )

        titles = [movie["title"] for movie in response.context["movies"]]
        self.assertEqual(titles, ["Интерстеллар", "Начало"])

    def test_search_by_title(self) -> None:
        response = self.client.get(reverse("catalog:search"), {"q": "Матр"})

        titles = [movie["title"] for movie in response.context["movies"]]
        self.assertEqual(titles, ["Матрица"])

    def test_search_value_is_not_part_of_sql(self) -> None:
        response = self.client.get(
            reverse("catalog:search"),
            {"q": "' OR 1=1 --"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["movies"]), 0)
        self.assertContains(response, "фильмы не найдены")
