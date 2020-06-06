from django.shortcuts import render
from django.views import View
from .models import Author


class AuthorDetail(View):
    def get(self, request, slug):
        # slug = self.kwargs['slug']
        author = Author.objects.get(slug=slug)
        return render(request, 'author/author.html', {'author': author})


