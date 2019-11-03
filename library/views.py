from django.shortcuts import render
from django.http import HttpResponse, Http404
from book.models import *
from user.models import *
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, reverse
from .utils import load_books_isbn, store_books

isbns = ['0399590595', '1982110562', '0735219095', '0062963678', '0525536612', '0385543786', '1501190628',
         '1250265703', '0062200674', '1538731339', '0399181393', '0451494342', '1629996297', '0525535276',
         '0525656154']


class Library(View):
    def get(self, request):
        no_photo = 'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png'
        # store_books()
        # books = Book.objects.filter(book_id='lkj')
        # for isbn in isbns:
        #     book = Book.objects.filter(book_id=isbn)
        #     print(book, 'yes')
        #     books |= book
        books = Book.objects.all().order_by('-average_rating').exclude(image=no_photo)[:30]
        valid_user = "False"
        all_users = list(CustomUser.objects.all())
        if not request.user.is_authenticated:
            timer = "yes"
        else:
            timer = "no"
        return render(request, 'library/library.html', {'books': books, 'valid_user': valid_user,
                                                        'timer': timer, 'error': False, 'all_users': all_users})

    def post(self, request):
        books = Book.objects.all()
        name = request.POST.get('name')
        password = request.POST.get('password')
        valid_user = "False"
        timer = "Not Exists"
        error = True
        all_users = list(CustomUser.objects.all())
        auth = authenticate(username=name, password=password)
        print(auth)
        if auth:
            login(request, auth)
            error = False
            valid_user = "True"
        return render(request, 'library/library.html', {'books': books, 'valid_user': valid_user,
                                                        'timer': timer, 'error': error, 'all_users': all_users})


class GenreDetail(View):
    def get(self, request, slug):
        # slug = self.kwargs['slug']
        book = Genre.objects.get(slug=slug)
        return render(request, 'library/genre.html', {'book': book})
