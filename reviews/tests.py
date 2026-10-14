from django.test import TestCase
from django.urls import reverse


class ReviewTests(TestCase):
    def test_review_list_opens(self) -> None:
        response = self.client.get(reverse("reviews:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_list.html")
        self.assertTemplateUsed(
            response,
            "reviews/includes/review_verdict.html",
        )
        self.assertContains(response, "Рекомендует")
        self.assertContains(response, "Не рекомендует")

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
