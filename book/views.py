from django.shortcuts import render
from django.http import HttpResponse, Http404
from book.models import *
from django.views.generic import View
from user.models import CustomUser, Comment, Review
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, reverse
from django.template.defaultfilters import linebreaks
from .utils import book_review_widget, post_review, get_review_id, delete_review, add_to_shelf
from user.models import Shelf
from learn.utils import view_utils as main_utils


class Detail(View):
    def get(self, request, book_id):
        try:
            valid_user = "False"
            book = Book.objects.get(book_id=book_id)
            reviews = book_review_widget(book)
            all_users = []
            # reviews = ''
            review = Review.objects.filter(book=book, user=request.user)
            if review:
                review = review[0]
            for user in CustomUser.objects.all():
                all_users.append(str(user.username))
            timer = "no"
            user = None
            shelves = Shelf.objects.filter(user=request.user)
            book_shelf = book.shelf_set.all()
            if not book_shelf:
                book_shelf = 0
            else:
                book_shelf = 1
            if request.user.is_authenticated:
                user = CustomUser.objects.filter(username=request.user.username)[0]
            # comments = Comment.objects.filter(book=book)
            comments = None
            similar_books = book.similar_books.all()
            return render(request, 'book/detail.html', {'comments': comments, 'book': book, 'valid_user': valid_user,
                                                        'timer': timer, 'error': False, 'all_users': all_users,
                                                        'user': user, 'similar_books': similar_books,
                                                        'reviews': reviews, 'shelves': shelves,
                                                        'review': review, 'book_shelf': book_shelf})
        except Book.DoesNotExist:
            raise Http404

    def post(self, request, book_id):
        try:
            book = Book.objects.get(book_id=book_id)
            valid_user = "False"
            error = True
            timer = "Not Exists"
            all_users = []
            reviews = book_review_widget(book)
            review = Review.objects.filter(book=book, user=request.user)
            # reviews = ''
            comments = Comment.objects.filter(book=book)
            user = None
            shelves = Shelf.objects.all()
            for user in CustomUser.objects.all():
                all_users.append(str(user.username))
            if request.user.is_authenticated:
                valid_user = "True"
                error = False
                # print('yes')
                text = request.POST.get('text')
                user = CustomUser.objects.filter(username=request.user.username)[0]
                Comment.objects.create(text=text, user=user, book=book)
                return redirect(reverse('detail', kwargs={'book_id': book.book_id}))
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
                       'user': user, 'reviews': reviews, 'shelves': shelves, 'review': review})


class ReviewCreate(View):
    def post(self, request, book_id):
        review = request.POST.get('review')
        shelf_name = request.POST.get('shelf')
        shelf = Shelf.objects.get(name=shelf_name, user=request.user)
        rating = request.POST.get('rating', 0)
        print(book_id)
        book = Book.objects.get(book_id=book_id)
        response = post_review(review, shelf_name, book.book_id, rating, request.user)
        if response.status_code == 201:
            review_id = get_review_id(response)
            a = Review.objects.create(review_id=review_id, body=review, rating=rating,
                                      user=request.user, book=book, shelf=shelf)
            shelf.books.add(book)
            print(a.review_id)
            return redirect(reverse('book:detail', kwargs={'book_id': book.book_id}))
        return HttpResponse('learn')


class ReviewDelete(View):
    def get(self, request, book_id):
        return main_utils.delete_review_view(book_id, 'book')


class AddToShelf(View):
    def post(self, request):
        print('hiii')
        shelf_name = request.POST.get('shelf')
        book_id = request.POST.get('book_id')
        shelf = Shelf.objects.get(name=shelf_name, user=request.user)
        response = add_to_shelf(shelf_name, book_id, request.user)
        print(response)
        book = Book.objects.get(book_id=book_id)
        if response.status_code == 201:
            if book.shelf_set.all():
                book.shelf_set.clear()
            shelf.books.add(book)
            return HttpResponse(book.title + ' is added to your shelf')
        return HttpResponse('learn')


class RemoveFromShelf(View):
    def get(self, request, book_id):
        return main_utils.delete_review_view(book_id, 'book', request.user.user_id, request.user)
