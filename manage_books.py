from db_connect import session
from db_create_table import Book
from sqlalchemy import update
from api_request import get_api_request
from db_create_table import book_attributes


def add_books(book_params):
    response_dict = get_api_request(book_params)
    if not response_dict:
        print('no matching books')
        return [-1, -1, -1]
    count_errors = 0
    count_duplicates = 0
    count_success = 0

    for info in response_dict['items']:
        vol = info['volumeInfo']
        curr_book = Book()

        try:
            isbn_pocket = vol.get('industryIdentifiers')
            for isbn_elem in isbn_pocket:
                if isbn_elem.get('type') == 'ISBN_13':
                    curr_book.ISBN = isbn_elem.get('identifier')
        except TypeError:
            print('no ISBN code!')
            count_errors += 1
            continue

        try:
            curr_book.title = vol.get('title', '<no title>')
        except TypeError:
            curr_book.title = '<no title>'

        try:
            authors = vol.get('authors')[0]
            for i in range(1, len(vol.get('authors'))):
                authors += ', ' + vol.get('authors')[i]
            curr_book.authors = authors
        except TypeError:
            curr_book.authors = '<no authors>'

        try:
            curr_book.publishedDate = vol.get('publishedDate', '<no publishedDate>')
        except TypeError:
            curr_book.publishedDate = '<no publishedDate>'

        try:
            curr_book.pageCount = vol.get('pageCount', None)
        except TypeError:
            curr_book.pageCount = None

        try:
            curr_book.thumbnail = vol.get('imageLinks').get('thumbnail', '<no thumbnail>')
        except (TypeError, AttributeError):
            curr_book.thumbnail = '<no thumbnail>'

        try:
            curr_book.language = vol.get('language', '<no language>')
        except TypeError:
            curr_book.language = '<no language>'

        query = session.query(Book.ISBN).filter(Book.ISBN == curr_book.ISBN).all()
        if len(query):
            print('Book already exists')
            count_duplicates += 1
        else:
            session.add(curr_book)
            session.commit()
            count_success += 1

    print('Books inserted')
    return [count_errors, count_duplicates, count_success]


def edit_book(book_target_isbn, book_config):

    if 'title' in book_config:
        stmt = update(Book).where(Book.ISBN == book_target_isbn).values(title=book_config['title']
                                                                        ).execution_options(synchronize_session="fetch")
        session.execute(stmt)
        session.commit()

    if 'authors' in book_config:
        stmt = update(Book).where(Book.ISBN == book_target_isbn).values(authors=book_config['authors']
                                                                        ).execution_options(synchronize_session="fetch")
        session.execute(stmt)
        session.commit()

    if 'publishedDate' in book_config:
        stmt = update(Book).where(Book.ISBN == book_target_isbn).values(publishedDate=book_config['publishedDate']
                                                                        ).execution_options(synchronize_session="fetch")
        session.execute(stmt)
        session.commit()

    if 'pageCount' in book_config:
        stmt = update(Book).where(Book.ISBN == book_target_isbn).values(pageCount=book_config['pageCount']
                                                                        ).execution_options(synchronize_session="fetch")
        session.execute(stmt)
        session.commit()

    if 'thumbnail' in book_config:
        stmt = update(Book).where(Book.ISBN == book_target_isbn).values(thumbnail=book_config['thumbnail']
                                                                        ).execution_options(synchronize_session="fetch")
        session.execute(stmt)
        session.commit()

    if 'language' in book_config:
        stmt = update(Book).where(Book.ISBN == book_target_isbn).values(language=book_config['language']
                                                                        ).execution_options(synchronize_session="fetch")
        session.execute(stmt)
        session.commit()


def get_books():
    query = session.query(Book.ISBN, Book.title, Book.authors, Book.publishedDate,
                          Book.pageCount, Book.thumbnail, Book.language).order_by(Book.ISBN).all()
    books = []
    for book in query:
        book_dict = dict(zip(book_attributes, book))
        books.append(book_dict)

    return books


def get_book_by_isbn(book_isbn):
    query = session.query(Book.ISBN, Book.title, Book.authors, Book.publishedDate,
                          Book.pageCount, Book.thumbnail, Book.language).filter(Book.ISBN == book_isbn).first()
    book_dict = dict(zip(book_attributes, query))

    return book_dict
