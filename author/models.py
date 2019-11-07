from django.db import models


class Author(models.Model):
    author_id = models.CharField(unique=True, max_length=20, default='0')
    slug = models.SlugField(unique=True, max_length=40)
    name = models.CharField(max_length=20)
    average_rating = models.FloatField(default=0)
    about = models.TextField(null=True)
    image = models.URLField(default='https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png')

    def __str__(self):
        return self.name
