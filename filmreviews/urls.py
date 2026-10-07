"""URL configuration for the film review web project."""

from django.contrib import admin
from django.urls import include, path

from homepage import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("movies/", include("catalog.urls")),
    path("reviews/", include("reviews.urls")),
]

handler404 = views.page_not_found
