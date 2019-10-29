from django.db import models


class Author(models.Model):
    author_id = models.CharField(unique=True, max_length=20, default='0')
    slug = models.SlugField(unique=True, max_length=40)
    name = models.CharField(max_length=20)
    average_rating = models.FloatField(default=0)
    about = models.TextField(null=True)
    image = models.URLField()

    def __str__(self):
        return self.name
