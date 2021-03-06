from goodreads import client
from rauth.service import OAuth1Service
from .models import Book
import xml.etree.ElementTree as et

consumer_key = 'ePqGSFb6Pt7Xll8EnFzQJA'
consumer_secret = 'Y7V0YdQpwW5908NGWna8GeAQWUEP6s4IK6fAQqb0JM'

goodreads = OAuth1Service(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        name='goodreads',
        request_token_url='https://www.goodreads.com/oauth/request_token',
        authorize_url='https://www.goodreads.com/oauth/authorize',
        access_token_url='https://www.goodreads.com/oauth/access_token',
        base_url='https://www.goodreads.com'
    )


def book_review_widget(book):
    gc = client.GoodreadsClient(consumer_key, consumer_secret)
    response = gc.book(book.book_id).reviews_widget
    print(response)
    return response


def post_review(review, shelf, book_id, rating, user):
    data = {'book_id': book_id, 'review[review]': review, 'review[rating]': rating, 'shelf': shelf}
    print(review, shelf, book_id)
    session = goodreads.get_session((user.access_token,
                                     user.access_token_secret))
    response = session.post('https://www.goodreads.com/review.xml', data)
    print(response, response.text)
    return response


def load_xml(response):
    with open('book/review.xml', 'wb') as f:
        f.write(response.content)


def get_review_id(response):
    load_xml(response)
    tree = et.parse('book/review.xml')
    review_id = ''
    root = tree.getroot()
    for review in root.iter('review'):
        for tag in review:
            tag_name = tag.tag
            tag_text = tag.text
            if tag_name == 'id':
                review_id = tag_text

        return review_id


def delete_review(book_id, shelf_name, user):
    # if shelf_name == 'read':
    #     print('added to delete')
    #     return add_to_shelf('delete', book_id, user)

    data = {'name': shelf_name, 'book_id': book_id, 'a': 'remove'}
    session = goodreads.get_session((user.access_token,
                                     user.access_token_secret))

    url = 'https://www.goodreads.com/shelf/add_to_shelf.xml'
    return session.post(url, data)


def add_to_shelf(shelf_name, book_id, user):
    data = {'name': shelf_name, 'book_id': book_id}
    url = 'https://www.goodreads.com/shelf/add_to_shelf.xml'
    session = goodreads.get_session((user.access_token,
                                     user.access_token_secret))
    return session.post(url, data)
