from django.urls import path
from book import views

app_name = 'book'
urlpatterns = [
    path('<slug:slug>/', views.Detail.as_view(), name='detail'),
]