from django.urls import path
from learn import settings
from . import views

app_name = 'user'
urlpatterns = [
    path('logout/', views.Logout.as_view(), name='logout'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('profile/<int:user_id>/', views.Profile.as_view(), name='profile'),
    path('profile/<int:user_id>/shelves/<int:shelf_id>', views.ShelfView.as_view(), name='shelves')
    # path('comment/', views.CommentPost.as_view(), name='comment')
]