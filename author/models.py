from django.db import models


class Author(models.Model):
    # pass
    author_id = models.CharField(unique=True, max_length=200, default='0')
    slug = models.SlugField(unique=True, max_length=400)
    name = models.CharField(max_length=200)
    average_rating = models.FloatField(default=0)
    about = models.TextField(null=True)
    image = models.URLField(default='https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png')

    def __str__(self):
        return self.name
