from django.db import models
from django.contrib.auth.models import AbstractUser
from book.models import Book

rating_choices = (
    (0, 'no rating'),
    (1, 'did not like it'),
    (2, 'it was ok'),
    (3, 'liked it'),
    (4, 'really liked it'),
    (5, 'it was amazing')
)


class Status(models.Model):
    status_id = models.CharField(max_length=20)
    type = models.CharField(max_length=200)
    action_text = models.CharField(max_length=500)
    updated_at = models.CharField(max_length=100)
    body = models.TextField(null=True)
    image = models.URLField()

    def __str__(self):
        return self.action_text


class Shelf(models.Model):
    shelf_id = models.CharField(unique=True, max_length=200)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    review_id = models.CharField(unique=True, max_length=20)
    body = models.TextField()
    rating = models.PositiveIntegerField(choices=rating_choices, default=3)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.rating, self.body)


class CustomUser(AbstractUser):
    user_id = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=500, default='')
    interests = models.CharField(max_length=700, null=True)
    fav_books = models.CharField(max_length=700, null=True)
    best_quote = models.CharField(max_length=720, null=True)
    friends_count = models.IntegerField(default=0)
    reviews_count = models.IntegerField(default=0)
    image = models.URLField(blank=True)

    def __str__(self):
        return self.username


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
