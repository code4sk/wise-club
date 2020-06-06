from django.shortcuts import render
from django.http import Http404
from django.views.generic import View


class Home(View):
    def get(self, request):
        return render(request, 'home/home.html')


class MiddlewareFactory:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print(exception)

        if isinstance(exception, Http404):
            return render(request, 'home/exception.html', {})
        else:
            return render(request, 'home/exception500.html', {})
