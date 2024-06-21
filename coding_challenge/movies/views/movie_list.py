from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from movies.models import Movie, Review
from movies.serializers import MovieSerializer, ReviewSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


class MovieFilter(filters.FilterSet):
    """Filter movies based on runtime."""

    runtime_longer_than = filters.NumberFilter(field_name="runtime", lookup_expr="gt")
    runtime_shorter_than = filters.NumberFilter(field_name="runtime", lookup_expr="lt")

    class Meta:
        model = Movie
        fields = ["runtime_longer_than", "runtime_shorter_than"]


class MovieListView(ListCreateAPIView):
    """List all movies or add a new movie to the list. Filter options are available
    based on runtime."""

    serializer_class = MovieSerializer
    queryset = Movie.objects.order_by("id")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieFilter
    ordering_fields = ["runtime"]


class MovieDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a movie instance."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewListCreateView(ListCreateAPIView):
    """List all reviews or create a new review."""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Return all reviews for a movie."""
        movie_id = self.kwargs["movie_id"]
        return Review.objects.filter(movie_id=movie_id)

    def perform_create(self, serializer):
        """Create a new review."""
        movie_id = self.kwargs["movie_id"]
        movie = get_object_or_404(Movie, id=movie_id)
        serializer.save(movie=movie)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a review instance."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_object(self):
        """Return a review for a movie."""
        movie_id = self.kwargs["movie_id"]
        review_id = self.kwargs["pk"]
        return get_object_or_404(Review, movie_id=movie_id, id=review_id)
