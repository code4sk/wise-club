from django.urls import path
from library import views

app_name = 'library'
urlpatterns = [
    path('', views.Library.as_view(), name='library'),
    path('genre/<slug:slug>/', views.GenreDetail.as_view(), name='genre'),
]
