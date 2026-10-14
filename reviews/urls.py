from django.urls import path

from reviews import views


app_name = "reviews"

urlpatterns = [
    path("", views.review_list, name="list"),
    path("<int:review_id>/", views.review_detail, name="detail"),
]
