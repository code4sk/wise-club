from django.urls import path
from library import views

app_name = 'library'
urlpatterns = [
    path('', views.Library.as_view(), name='library'),
    path('search/', views.SearchBook.as_view(), name='search_book'),
    path('genre/<slug:slug>/', views.GenreDetail.as_view(), name='genre'),
]
