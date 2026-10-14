from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from services import find_review_by_id, get_latest_reviews
from storage import load_system


def review_list(request: HttpRequest) -> HttpResponse:
    system = load_system()
    context = {
        "reviews": get_latest_reviews(
            system.reviews,
            limit=len(system.reviews),
        ),
    }
    return render(request, "reviews/review_list.html", context)


def review_detail(request: HttpRequest, review_id: int) -> HttpResponse:
    system = load_system()
    review = find_review_by_id(system.reviews, review_id)
    context = {
        "review": review,
    }
    return render(
        request,
        "reviews/review_detail.html",
        context,
        status=404 if review is None else 200,
    )
