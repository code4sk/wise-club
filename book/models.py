from django.db import models
from author.models import Author


types = (
    ('I', 'ISBN'),
    ('G', 'GID')
)


class Genre(models.Model):
    genre_id = models.CharField(unique=True, max_length=20, default='0')
    slug = models.SlugField(unique=True, max_length=40)
    name = models.CharField(max_length=25)
    info = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    type = models.CharField(choices=types, max_length=1, default='I')
    book_id = models.CharField(unique=True, max_length=200, default='0')
    slug = models.SlugField(unique=True, max_length=400)
    title = models.CharField(max_length=250, null=True)
    average_rating = models.FloatField(default=0)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre, blank=True)
    description = models.TextField(default='', null=True)
    similar_books = models.ManyToManyField('Book', blank=True)
    image = models.URLField()

    def __str__(self):
        return self.title
