from django.urls import path

from reviews import views


urlpatterns = [
    path("", views.review_list, name="review_list"),
    path("<int:review_id>/", views.review_detail, name="review_detail"),
]
