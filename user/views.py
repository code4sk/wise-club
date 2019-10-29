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
from .utils import get_user_data, get_shelf_data
from .models import Status


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
