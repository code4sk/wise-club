from django.urls import path
from author import views

app_name = 'author'
urlpatterns = [
    path('<slug:slug>/', views.AuthorDetail.as_view(), name='author'),
]
