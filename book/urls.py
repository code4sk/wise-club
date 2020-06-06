# from django.urls import path
# from book import views
#
# app_name = 'book'
# urlpatterns = [
#     path('<str:book_id>/', views.Detail.as_view(), name='detail'),
#     path('review/create/<str:book_id>', views.ReviewCreate.as_view(), name='review'),
#     path('review/delete/<str:book_id>/review', views.ReviewDelete.as_view(), name='review_delete'),
#     path('add-to-shelf', views.AddToShelf.as_view(), name='add_to_shelf'),
#     path('remove-from-shelf/<str:book_id>', views.RemoveFromShelf.as_view(), name='remove_from_shelf')
# ]