from django.urls import reverse

from db.testing import TemporaryDatabaseTestCase


class ReviewTests(TemporaryDatabaseTestCase):
    def test_review_list_opens(self) -> None:
        response = self.client.get(reverse("reviews:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_list.html")
        self.assertTemplateUsed(
            response,
            "reviews/includes/review_verdict.html",
        )
        self.assertEqual(len(response.context["reviews"]), 7)
        self.assertContains(response, "Рекомендует")
        self.assertContains(response, "Не рекомендует")

    def test_review_list_filter_by_verdict(self) -> None:
        response = self.client.get(
            reverse("reviews:list"),
            {"recommended": "0"},
        )

        reviews = response.context["reviews"]
        self.assertEqual([review["id"] for review in reviews], [4])

    def test_review_detail_opens(self) -> None:
        response = self.client.get(reverse("reviews:detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_detail.html")
        self.assertContains(response, "Сильная научная фантастика")
        self.assertContains(response, "22.09.2026")

    def test_missing_review_returns_404(self) -> None:
        response = self.client.get(reverse("reviews:detail", args=[999]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Отзыв не найден", status_code=404)

    def test_statistics_page(self) -> None:
        response = self.client.get(reverse("reviews:statistics"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/statistics.html")
        self.assertEqual(response.context["totals"]["reviews_count"], 7)
        genres = {row["genre"]: row for row in response.context["genres"]}
        self.assertEqual(genres["Фантастика"]["movies_count"], 3)
        self.assertEqual(len(response.context["popular_movies"]), 3)

    def test_statistics_having_threshold(self) -> None:
        response = self.client.get(
            reverse("reviews:statistics"),
            {"min_reviews": "3"},
        )

        self.assertEqual(len(response.context["popular_movies"]), 0)
        self.assertContains(response, "Фильмов с таким числом отзывов нет")
