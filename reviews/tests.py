from django.test import TestCase
from django.urls import reverse


class ReviewTests(TestCase):
    def test_review_list_opens(self) -> None:
        response = self.client.get(reverse("review_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отзывы")

    def test_review_detail_opens(self) -> None:
        response = self.client.get(reverse("review_detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сильная научная фантастика")

    def test_missing_review_returns_404(self) -> None:
        response = self.client.get(reverse("review_detail", args=[999]))

        self.assertEqual(response.status_code, 404)
