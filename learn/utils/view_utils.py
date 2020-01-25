from book import utils as book_utils
from book.models import Book
from user.models import Review, Shelf
from django.shortcuts import redirect, reverse, HttpResponse


def delete_review_view(book_id, redirect_to, shelf_id=7, user_id=97134500):
    print('ok')
    book = Book.objects.get(book_id=book_id)
    shelf_name = book.shelf_set.all()[0].name
    response = book_utils.delete_review(book.book_id, shelf_name)
    print(response.text)
    review = Review.objects.filter(book=book)
    if response.status_code == 200:
        if review:
            review[0].delete()
        book.shelf_set.clear()
        if redirect_to == 'book':
            return redirect(reverse('book:detail', kwargs={'book_id': book.book_id}))
        else:
            return redirect(reverse('user:shelves', kwargs={'user_id': user_id, 'shelf_id': shelf_id}))
    return HttpResponse('learn ' + str(response.status_code))
