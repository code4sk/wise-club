from django.urls import path
from learn import settings
from . import views

app_name = 'user'
urlpatterns = [
    path('logout/', views.Logout.as_view(), name='logout'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('profile/<int:user_id>/', views.Profile.as_view(), name='profile'),
    path('profile/<int:user_id>/shelves/<int:shelf_id>', views.ShelfView.as_view(), name='shelves'),
    path('<str:user_id>/shelf/<str:shelf_id>/book/<str:book_id>/remove',
         views.ShelfRemoveBook.as_view(), name='book_remove'),
    path('review<str:review_id>/edit', views.EditReview.as_view(), name='edit_review'),
    # path('comment/', views.CommentPost.as_view(), name='comment')
]