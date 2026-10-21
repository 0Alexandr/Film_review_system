from django.urls import path

from catalog import views


app_name = "catalog"

urlpatterns = [
    path("", views.movie_list, name="list"),
    path("search/", views.movie_search, name="search"),
    path("<int:movie_id>/", views.movie_detail, name="detail"),
]
