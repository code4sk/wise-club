from goodreads import client
import requests
from book.models import Book
from author.models import Author
from django.template.defaultfilters import slugify

author_ids = list(Author.objects.values_list('author_id', flat=True))
book_ids = list(Book.objects.values_list('book_id', flat=True))
consumer_key = 'ePqGSFb6Pt7Xll8EnFzQJA'
consumer_secret = 'Y7V0YdQpwW5908NGWna8GeAQWUEP6s4IK6fAQqb0JM'


def create_book(b, isbn=0):
    print('come')
    slug = slugify(b.title)
    # if isbn == 0:
    b_isbn = b.isbn
    # else:
    #     b_isbn = isbn
    gc = client.GoodreadsClient(consumer_key, consumer_secret)
    if not b_isbn:
        b_isbn = b.gid
    book = Book.objects.create(book_id=b_isbn, title=b.title, description=b.description, image=b.image_url,slug=slug)
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
            book = create_book(b, isbn)
        else:
            print('already')
            book = Book.objects.filter(book_id=b.isbn)[0]
        try:
            similar_books = b.similar_books[0:5]
        except :
            similar_books = None
        if similar_books:
            for similar in similar_books:
                sim_id = similar.isbn
                if not sim_id:
                    continue
                if sim_id not in book_ids:
                    sim_b = create_book(gc.book(isbn=sim_id))
                else:
                    sim_b = Book.objects.filter(book_id=sim_id)[0]
                if sim_b:
                    book.similar_books.add(sim_b)
                    sim_b.similar_books.add(book)
        print(book)
