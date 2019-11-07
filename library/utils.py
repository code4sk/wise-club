from goodreads import client
import requests
from book.models import Book
from author.models import Author
from goodreads.session import OAuth1Service
from django.template.defaultfilters import slugify
from xml.etree import ElementTree as et
import threading

author_ids = list(Author.objects.values_list('author_id', flat=True))
book_ids = list(Book.objects.values_list('book_id', flat=True))
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


def create_book(b, isbn=0):
    print('come')
    slug = slugify(b.title + '-' + b.gid)
    # if isbn == 0:
    b_isbn = b.gid
    # else:
    #     b_isbn = isbn
    gc = client.GoodreadsClient(consumer_key, consumer_secret)
    book = Book.objects.create(book_id=b_isbn, title=b.title, average_rating=b.average_rating, description=b.description, image=b.image_url,slug=slug)
    authors = b.authors
    for author in authors:
        author_slug = slugify(author.name)
        if author.gid not in author_ids:
            about = gc.author(author.gid).about
            a = Author.objects.create(author_id=author.gid, name=author.name,
                                      image=dict(author.image_url)['#text'], slug=author_slug, about=about)
            book.author.add(a)
            author_ids.append(author.gid)
        else:
            book.author.add(Author.objects.get(author_id=author.gid))
    book_ids.append(b_isbn)
    print('exit')
    return book


def load_books_isbn():
    base_url = 'https://api.nytimes.com/svc/books/v3/lists.json'
    list_type = 'hardcover-fiction'
    api_key = 'ITB9AqB2ckRfgB75FSI1ZCD3MROk9nIT'
    url = '{}?list={}&api-key={}'.format(base_url, list_type, api_key)
    response = requests.get(url)
    response = response.json()
    isbns = []
    print('ok')
    for i in range(0, 15):
        isbns.append(response['results'][i]['isbns'][0]['isbn10'])
    return isbns


def store_books():
    isbns = load_books_isbn()
    # isbns = ['9780399590597', '9781982110567', '9780735219090', '9780062963673', '9780525536611', '9780385543781', '9781501190629', '9781250265708', '9780062200679', '9781538731338']
    # gc.authenticate(access_token, access_token_secret)
    for isbn in isbns:
        gc = client.GoodreadsClient(consumer_key, consumer_secret)
        b = gc.book(isbn=isbn)
        if b.isbn not in book_ids:
            book = create_book(b)
        else:
            print('already')
            book = Book.objects.filter(book_id=b.gid)[0]
        try:
            similar_books = b.similar_books[0:5]
        except :
            similar_books = None
        if similar_books:
            for similar in similar_books:
                sim_id = similar.gid
                if not sim_id:
                    continue
                if sim_id not in book_ids:
                    sim_b = create_book(gc.book(sim_id))
                else:
                    sim_b = Book.objects.filter(book_id=sim_id)[0]
                if sim_b:
                    book.similar_books.add(sim_b)
                    sim_b.similar_books.add(book)
        print(book)


def load_search_xml(text):
    data = {'q': text, 'key': consumer_key, 'search[field]': 'title'}
    url = 'https://www.goodreads.com/search/index.xml'
    response = session.get(url, params=data)
    with open('library/search.xml', 'wb') as f:
        f.write(response.content)


def load_search_data(text):
    load_search_xml(text)
    books = []
    tree = et.parse('library/search.xml')
    root = tree.getroot()
    for users in root.iter('results'):
        for tag in users:
            tag_name = tag.tag
            if tag_name == 'work':
                for update in tag:
                    # print(update.tag)
                    if update.tag == 'best_book':
                        book = {}
                        for book_tag in update:
                            if book_tag.tag == 'id':
                                book['id'] = book_tag.text
                            if book_tag.tag == 'title':
                                book['title'] = book_tag.text
                            if book_tag.tag == 'image_url':
                                book['image_url'] = book_tag.text
                            if book_tag.tag == 'author':
                                for props in book_tag:
                                    if props.tag == 'id':
                                        book['author_id'] = props.text
                                    if props.tag == 'name':
                                        book['author_name'] = props.text
                        books.append(book)
        # print(books)
        print('------------XXXX------------')
        return books


class MyThread(threading.Thread):
    def __init__(self, name, books):
        threading.Thread.__init__(self)
        self.name = name
        self.books = books

    def run(self):
        gc = client.GoodreadsClient(consumer_key, consumer_secret)
        for book in self.books:
            if book['id'] not in book_ids:
                b = gc.book(book['id'])
                create_book(b)
                print(b.title, b.authors[0].name)
        print('END OF "{}"'.format(self.name))


def search_book(text):
    # gc = client.GoodreadsClient(consumer_key, consumer_secret)
    # print(gc.search_books(text))
    books = load_search_data(text)
    t1 = MyThread('one', books)
    t1.start()
    return books

