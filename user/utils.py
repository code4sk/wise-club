import requests
from goodreads import client
import xml.etree.ElementTree as et
from django.template.defaultfilters import slugify
from user.models import Status, Shelf, Review, CustomUser
from rauth.service import OAuth1Service
from library.utils import create_book
from book.models import Book
from author.models import Author

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

session = goodreads.get_session(('RCyAWcTakiGfmAcdg2jHUw',
                                 'Tcpw1wIlc1QbbOCkRgMflEc66WDks7pj1NQ4AB4X4'))


def load_xml():
    url = 'https://www.goodreads.com/user/show/97134500.xml?key=ePqGSFb6Pt7Xll8EnFzQJA'
    response = requests.get(url)
    with open('user/user.xml', 'wb') as f:
        f.write(response.content)


def load_friend_xml():
    data = {'id': 97134500}
    url = 'https://www.goodreads.com/friend/user.xml'
    response = session.get(url, params=data)
    with open('user/friend.xml', 'wb') as f:
        f.write(response.content)


def load_shelf_xml():
    data = {'id': 97134500, 'key': consumer_key}
    url = 'https://www.goodreads.com/review/list?v=2'
    response = session.get(url, params=data)
    with open('user/shelf.xml', 'wb') as f:
        f.write(response.content)


def load_friend_data():
    # load_friend_xml()
    friends = []
    tree = et.parse('user/friend.xml')
    root = tree.getroot()
    for friend in root.iter('friends'):
        for tag in friend:
            if tag.tag == 'user':
                friend = {}
                for prop in tag:
                    if prop.tag == 'id':
                        friend['id'] = prop.text
                    if prop.tag == 'name':
                        friend['name'] = prop.text
                    if prop.tag == 'image_url':
                        friend['image_url'] = prop.text
                    if prop.tag == 'reviews_count':
                        friend['reviews_count'] = prop.text
                    if prop.tag == 'friends_count':
                        friend['friends_count'] = prop.text
                friends.append(friend)

        # print(friends)
        # print('------------XXXX------------')
        return friends


def load_user_data():
    load_xml()
    name = ''
    image_url = ''
    about = ''
    interests = ''
    favorite_books = ''
    user_shelves = []
    user_statuses = []
    tree = et.parse('user/user.xml')
    root = tree.getroot()
    for users in root.iter('user'):
        for tag in users:
            tag_name = tag.tag
            tag_text = tag.text
            if tag_name == 'image_url':
                image_url = tag_text
            if tag_name == 'name':
                name = tag_text
            if tag_name == 'about':
                about = tag_text
            if tag_name == 'interests':
                interests = tag_text
            if tag_name == 'favourite_books':
                favorite_books = tag_text
            if tag_name == 'user_shelves':
                for user_shelf in tag:
                    shelf = {}
                    for prop in user_shelf:
                        if prop.tag == 'id':
                            shelf['id'] = prop.text
                        if prop.tag == 'name':
                            shelf['name'] = prop.text
                        if prop.tag == 'description':
                            shelf['description'] = prop.text
                        if prop.tag == 'book_count':
                            shelf['book_count'] = prop.text
                    user_shelves.append(shelf)
            if tag_name == 'updates':
                for update in tag:
                    status = {'type': update.attrib['type']}
                    for stat in update:
                        if stat.tag == 'action_text':
                            status['action_text'] = stat.text
                        if stat.tag == 'link':
                            status['link'] = stat.text
                        if stat.tag == 'updated_at':
                            status['updated_at'] = stat.text
                        if stat.tag == 'image_url':
                            status['image_url'] = stat.text
                        if stat.tag == 'body':
                            status['body'] = stat.text
                        if stat.tag == 'object':
                            for obj in stat:
                                for stat_info in obj:
                                    if stat_info.tag == 'id':
                                        status['id'] = stat_info.text
                                    # if stat_info.tag == 'book_id':
                                    #     status['book_id'] = stat_info.text
                                    # if stat_info.tag == 'page':
                                    #     status['page'] = stat_info.text
                                    # if stat_info.tag == 'percent':
                                    #     status['percent'] = stat_info.text
                                    # if stat_info.tag == 'body':
                                    #     status['body'] = stat_info.text
                                    # print(stat_info.tag, stat_info.text)
                    user_statuses.append(status)
        # print(user_statuses)
        # print('------------XXXX------------')
        return [name, image_url, interests,favorite_books  , about, user_shelves, user_statuses]


def load_shelf_data():
    load_shelf_xml()
    shelves = []
    shelves_id = {}
    tree = et.parse('user/shelf.xml')
    root = tree.getroot()
    for reviews in root.iter('reviews'):
        for tag in reviews:
            if tag.tag == 'review':
                shelf = {'author': []}
                for prop in tag:
                    if prop.tag == 'id':
                        shelf['review_id'] = prop.text
                    if prop.tag == 'book':
                        for book in prop:
                            # print(book.tag)
                            if book.tag == 'id':
                                shelf['book_id'] = book.text
                            if book.tag == 'title':
                                shelf['title'] = book.text
                                print(shelf['title'])
                            if book.tag == 'image_url':
                                shelf['image_url'] = book.text
                            if book.tag == 'description':
                                shelf['description'] = book.text
                            if book.tag == 'average_rating':
                                shelf['average_rating'] = book.text
                            if book.tag == 'authors':
                                for author in book:
                                    author_dict = {}
                                    if author.tag == 'author':
                                        for author_prop in author:
                                            if author_prop.tag == 'id':
                                                # print('ok')
                                                author_dict['author_id'] = author_prop.text
                                            if author_prop.tag == 'name':
                                                author_dict['name'] = author_prop.text
                                            if author_prop.tag == 'image_url':
                                                author_dict['image_url'] = author_prop.text
                                            if author_prop.tag == 'average_rating':
                                                author_dict['average_rating'] = author_prop.text
                                        shelf['author'].append(author_dict)
                    if prop.tag == 'rating':
                        shelf['rating'] = prop.text
                    if prop.tag == 'shelves':
                        for s in prop:
                            if s.tag == 'shelf':
                                shelf['id'] = s.attrib['id']
                                shelf['name'] = s.attrib['name']
                    if prop.tag == 'body':
                        shelf['body'] = prop.text
                shelves.append(shelf)
        # print(shelves)
        print('------------XXXX------------')
        return shelves


def get_status(user_statuses):
    statuses = []
    for stat in user_statuses:
        status_type = stat.get('type')
        status_id = stat.get('link').split('/')[-1]
        image_url = stat.get('image_url')
        action_text = stat.get('action_text')
        updated_at = (stat.get('updated_at').split('-'))[0]
        body = stat.get('body')
        if action_text != 'liked a quote':
            query = Status.objects.filter(action_text=action_text)
        else:
            query = Status.objects.filter(body=body)
        if not query:
            s = Status.objects.create(status_id=status_id, type=status_type, image=image_url, action_text=action_text,
                                      updated_at=updated_at, body=body)
        else:
            s = query[0]
        statuses.append(s)
    return statuses


def get_friends(friends_list):
    friends = []
    for friend in friends_list:
        # print(friend)
        if friend.get('id') not in CustomUser.objects.values_list('user_id', flat=True):
            username = friend.get('id')
            s = CustomUser.objects.create(username=username, user_id=friend.get('id'), name=friend.get('name'),
                                          image=friend.get('image_url'),
                                          reviews_count=friend.get('reviews_count'),
                                          friends_count=friend.get('friends_count'))
        else:
            s = CustomUser.objects.filter(user_id=friend.get('id'))[0]
        friends.append(s)
    return friends


def get_shelves(shelves):
    all_shelves_model = []
    for shelf in shelves:
        # print(shelf)
        shelf_id = shelf.get('id')
        book_id = shelf.get('book_id')
        title = shelf.get('title')
        average_rating = shelf.get('average_rating')
        image_url = shelf.get('image_url')
        description = shelf.get('description')
        shelf_model = Shelf.objects.get(shelf_id=shelf_id)
        book_list = list(Book.objects.values_list('book_id', flat=True))
        # print(book_list)
        if book_id not in book_list:
            # print(title)
            slug = slugify(title)
            book = Book.objects.create(book_id=book_id, slug=slug, title=title,
                                       image=image_url, description=description,
                                       average_rating=average_rating)
            for single_author in shelf.get('author'):
                author_id = single_author.get('author_id')
                author_name = single_author.get('name')
                author_image_url = single_author.get('image_url')
                author_average_rating = single_author.get('average_rating')
                author_list = Author.objects.values_list('author_id', flat=True)
                if author_id not in author_list:
                    author = Author.objects.create(author_id=author_id, name=author_name,
                                                   image=author_image_url, slug=slugify(author_name),
                                                   average_rating=author_average_rating)
                else:
                    author = Author.objects.get(author_id=author_id)
                # print(author.name)
                book.author.add(author)
        else:
            book = Book.objects.get(book_id=book_id)
            # print(book)
        if book not in shelf_model.books.all():
            shelf_model.books.add(book)
        user = CustomUser.objects.get(user_id=97134500)
        if shelf.get('review_id') not in Review.objects.values_list('review_id', flat=True):
            review = Review.objects.create(review_id=shelf.get('review_id'), body=shelf.get('body'),
                                           rating=shelf.get('rating'), book=book, shelf=shelf_model, user=user)
        all_shelves_model.append(shelf_model)
    return all_shelves_model


def get_user_shelves(user_shelves):
    shelves = []
    for shelf in user_shelves:
        # print(shelf)
        if shelf.get('id') not in Shelf.objects.values_list('shelf_id', flat=True):
            user = CustomUser.objects.get(user_id=97134500)
            s = Shelf.objects.create(shelf_id=shelf.get('id'), name=shelf.get('name'), user=user)
        else:
            s = Shelf.objects.filter(shelf_id=shelf.get('id'))[0]
        shelves.append(s)
    return shelves


def get_user_data():
    [name, image_url, interests, favourite_books, about, user_shelves, user_statuses] = load_user_data()
    friends = load_friend_data()
    return [get_status(user_statuses), get_user_shelves(user_shelves), get_friends(friends)]


def get_shelf_data():
    shelves = load_shelf_data()
    return get_shelves(shelves)
