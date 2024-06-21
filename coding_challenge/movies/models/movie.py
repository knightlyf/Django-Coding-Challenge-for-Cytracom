from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    runtime = models.PositiveIntegerField()
    release_date = models.DateField()

    def __str__(self):
        """Return the title of the movie"""
        return self.title

    @property
    def runtime_formatted(self):
        """Return the runtime in hours and minutes"""
        hours, minutes = divmod(self.runtime, 60)
        return f"{hours}:{minutes:02d}"

    @property
    def avg_rating(self):
        """Return the average rating for the movie"""
        reviews = self.reviews.all()
        if reviews:
            total = sum([review.rating for review in reviews])
            return total / len(reviews)
        return 0

    @property
    def reviewers(self):
        """Return the reviewers for the movie"""
        return [{review.name, review.rating} for review in self.reviews.all()]


class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.rating})"
