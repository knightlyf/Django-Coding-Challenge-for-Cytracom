from django.urls import path

from movies.views import (
    MovieListView,
    MovieDetailView,
    ReviewListCreateView,
    ReviewDetailView,
)

urlpatterns = [
    path("", MovieListView.as_view(), name="MovieListView"),
    path("<int:pk>", MovieDetailView.as_view(), name="MovieDetailView"),
    path(
        "<int:movie_id>/reviews",
        ReviewListCreateView.as_view(),
        name="ReviewListCreateView",
    ),
    path(
        "<int:movie_id>/reviews/<int:pk>",
        ReviewDetailView.as_view(),
        name="ReviewDetailView",
    ),
]
