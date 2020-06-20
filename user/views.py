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
from .utils import load_user_id_data, get_user_data, get_shelf_data, edit_review
from .models import Status
from learn.utils import view_utils as main_utils
from rauth.service import OAuth1Service, OAuth1Session
import requests
from django.http import HttpResponseRedirect


CONSUMER_KEY = 'ePqGSFb6Pt7Xll8EnFzQJA'
CONSUMER_SECRET = 'Y7V0YdQpwW5908NGWna8GeAQWUEP6s4IK6fAQqb0JM'

goodreads = OAuth1Service(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    name='goodreads',
    request_token_url='https://www.goodreads.com/oauth/request_token',
    authorize_url='https://www.goodreads.com/oauth/authorize',
    access_token_url='https://www.goodreads.com/oauth/access_token',
    base_url='https://www.goodreads.com/'
)


class Profile(View):
    def get(self, request, user_id):
        # print(request.user.image)
        [statuses, user_shelves, friends] = get_user_data(request.user)
        user_quotes = [status for status in statuses if status.type == 'userquote']
        return render(request, 'user/profile.html', {'statuses': statuses, 'user_shelves': user_shelves,
                                                     'user_quotes': user_quotes, 'friends': friends})


class ShelfView(View):
    def get(self, request, user_id, shelf_id):
        get_shelf_data(request.user)
        shelf = Shelf.objects.filter(shelf_id=shelf_id, user=request.user)[0]
        reviews = Review.objects.filter(shelf=shelf, user=request.user)
        shelves = Shelf.objects.filter(user=request.user).exclude(name='delete')
        return render(request, 'user/shelves.html', {'shelves': shelves, 'reviews': reviews})


class ShelfRemoveBook(View):
    def get(self, request, book_id, shelf_id, user_id):
        return main_utils.delete_review_view(book_id, 'shelf', user_id, request.user)


class Logout(View):
    def get(self, request):
        logout(request)
        # print(self.request.GET.get('next'))
        return redirect('library:library')


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
            request_token, request_token_secret = goodreads.get_request_token(header_auth=True)
            # user = CustomUser.objects.filter(username=username)
            user = CustomUser.objects.create(username=username, password=password, request_token=request_token,
                                             request_token_secret=request_token_secret)
            authorize_url = goodreads.get_authorize_url(request_token)
            return HttpResponseRedirect(authorize_url)


class CallbackView(View):
    def get(self, request):
        user = CustomUser.objects.none()
        try:
            print('in callback')
            print(request.GET)
            request_token = request.GET.get('oauth_token')
            user = CustomUser.objects.get(request_token=request_token)
            if str(request.GET.get('authorize')) == '0':
                user.delete()
                return redirect('library:library')
            session = goodreads.get_auth_session(request_token, user.request_token_secret)
            user.access_token = session.access_token
            user.access_token_secret = session.access_token_secret
            user.save()
            print('now getting user id')
            load_user_id_data(session, user)
            login(request, user)
            return redirect('library:library')
        except Exception as e:
            print(e)
            user.delete()
            return HttpResponse('Some error occured while getting access token')


class EditReview(View):
    def get(self, request, review_id):
        review = Review.objects.get(review_id=review_id)
        print(review.body)
        text = review.body.replace("<br />",  '\n')
        text = text.strip()
        shelves = Shelf.objects.filter(user=request.user).exclude(name='delete')
        return render(request, 'user/review.html', {'review': review, 'text': text, 'shelves': shelves})

    def post(self, request, review_id):
        review = Review.objects.get(review_id=review_id)
        text = request.POST.get('review')
        rating = request.POST.get('rating')
        shelf_name = request.POST.get('shelf')
        shelf = Shelf.objects.get(name=shelf_name, user=request.user)
        book = review.book
        response = edit_review(review_id, text, rating, shelf_name, request.user)
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
