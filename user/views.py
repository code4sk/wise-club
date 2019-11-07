from django.shortcuts import render
from django.views.generic import View
from .forms import SignUpForm
from book.models import Book
from django.http import HttpResponse
from django.shortcuts import reverse
from django.shortcuts import redirect
from user.models import CustomUser, Review, Shelf
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from .utils import get_user_data, get_shelf_data, edit_review
from .models import Status
from learn.utils import view_utils as main_utils
import requests


class Profile(View):
    def get(self, request, user_id):
        # print(request.user.image)
        [statuses, user_shelves, friends] = get_user_data()
        user_quotes = [status for status in statuses if status.type == 'userquote']
        return render(request, 'user/profile.html', {'statuses': statuses, 'user_shelves': user_shelves,
                                                     'user_quotes': user_quotes, 'friends': friends})


class ShelfView(View):
    def get(self, request, user_id, shelf_id):
        get_shelf_data()
        shelf = Shelf.objects.filter(shelf_id=shelf_id)[0]
        reviews = Review.objects.filter(shelf=shelf)
        shelves = Shelf.objects.all()
        return render(request, 'user/shelves.html', {'shelves': shelves, 'reviews': reviews})


class ShelfRemoveBook(View):
    def get(self, request, book_id, shelf_id, user_id):
        return main_utils.delete_review_view(book_id, 'shelf', shelf_id, user_id)


class Logout(View):
    def get(self, request):
        logout(request)
        # print(self.request.GET.get('next'))
        return redirect(request.GET.get('next'))


class SignUp(View):
    def get(self, request):
        all_users = []
        for user in CustomUser.objects.all():
            all_users.append(str(user.username))
        return render(request, 'user/sign-up.html', {'all_users': all_users})

    def post(self, request):
        username = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        email = request.POST.get('email')
        name = request.POST.get('name')
        print(username)
        l = []
        for i in CustomUser.objects.all():
            l.append(i.username)
        if username in l:
            return render(request, 'user/sign-up.html', {'error': 'Username already exists'})
        elif pass1 != pass2:
            return render(request, 'user/sign-up.html', {'error': 'Password and Password Confirm is not Matching'})
        else:
            password = make_password(pass1)
            user = CustomUser.objects.create(username=username, email=email, password=password, name=name)
            login(request, user)
            return redirect('library')


class EditReview(View):
    def get(self, request, review_id):
        review = Review.objects.get(review_id=review_id)
        print(review.body)
        text = review.body.replace("<br />",  '\n')
        text = text.strip()
        shelves = Shelf.objects.all()
        return render(request, 'user/review.html', {'review': review, 'text': text, 'shelves': shelves})

    def post(self, request, review_id):
        review = Review.objects.get(review_id=review_id)
        text = request.POST.get('review')
        rating = request.POST.get('rating')
        shelf_name = request.POST.get('shelf')
        shelf = Shelf.objects.get(name=shelf_name)
        book = review.book
        response = edit_review(review_id, text, rating, shelf_name)
        print(response.text)
        if response.status_code == 200:
            review.body = text
            review.rating = rating
            review.shelf = shelf
            review.save()
            # data = {'book_id': book.book_id, 'shelf': shelf.shelf_id}
            # r1 = s.get(dhost)
            # csrf_token = r1.cookies['csrftoken']
            # response2 = requests.post('http://127.0.0.1:8000'+ reverse('book:add_to_shelf'), data=data)
            # print(response2)
            return redirect(reverse('user:shelves', kwargs={'user_id': request.user.user_id,
                                                            'shelf_id': shelf.shelf_id}))
        return HttpResponse('learn ' + str(response.status_code))
