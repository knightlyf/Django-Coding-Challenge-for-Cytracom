from rest_framework import serializers

from movies.models import Movie, Review


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ["id", "name", "rating"]

        def validate_rating(self, value):
            """Check that the rating is between 1 and 5."""
            if value < 1 or value > 5:
                raise serializers.ValidationError(
                    "Rating must be between 1 and 5 stars."
                )
            return value


class MovieSerializer(serializers.ModelSerializer):

    reviewers = serializers.ReadOnlyField()
    runtime_formatted = serializers.ReadOnlyField()
    avg_rating = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "runtime",
            "release_date",
            "runtime_formatted",
            "reviewers",
            "avg_rating",
        ]
        # fields = "__all__"
