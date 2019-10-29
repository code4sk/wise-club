from django.shortcuts import render
from django.http import HttpResponse, Http404
from book.models import *
from django.views.generic import View
from user.models import CustomUser, Comment
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, reverse
from django.template.defaultfilters import linebreaks


class Detail(View):
    def get(self, request, slug):
        try:
            valid_user = "False"
            book = Book.objects.get(slug=slug)
            all_users = []
            for user in CustomUser.objects.all():
                all_users.append(str(user.username))
            timer = "no"
            user = None
            if request.user.is_authenticated:
                user = CustomUser.objects.filter(username=request.user.username)[0]
            # comments = Comment.objects.filter(book=book)
            comments = None
            similar_books = book.similar_books.all()
            return render(request, 'book/detail.html', {'comments': comments, 'book': book, 'valid_user': valid_user,
                                                        'timer': timer, 'error': False, 'all_users': all_users,
                                                        'user': user, 'similar_books': similar_books})
        except Book.DoesNotExist:
            raise Http404

    def post(self, request, slug):
        try:
            book = Book.objects.get(slug=slug)
            valid_user = "False"
            error = True
            timer = "Not Exists"
            all_users = []
            comments = Comment.objects.filter(book=book)
            user = None
            for user in CustomUser.objects.all():
                all_users.append(str(user.username))
            if request.user.is_authenticated:
                valid_user = "True"
                error = False
                # print('yes')
                text = request.POST.get('text')
                user = CustomUser.objects.filter(username=request.user.username)[0]
                Comment.objects.create(text=text, user=user, book=book)
                return redirect(reverse('detail', kwargs={'slug': book.slug}))
            else:
                name = request.POST.get('name', None)
                if not name:
                    print('jlksfd')
                    return render(request, 'home/detail.html',
                                  {'comments': comments, 'book': book, 'valid_user': valid_user,
                                   'timer': timer, 'error': False, 'all_users': all_users})
                password = request.POST.get('password')
                auth = authenticate(username=name, password=password)
                error = True
                if auth:
                    login(request, auth)
                    error = False
                    user = CustomUser.objects.filter(username=request.user.username)[0]
                    valid_user = "True"
                # print('no')
        except Book.DoesNotExist:
            raise Http404
        return render(request, 'book/detail.html',
                      {'comments': comments, 'book': book, 'valid_user': valid_user,
                       'timer': timer, 'error': error, 'all_users': all_users,
                       'user': user})


