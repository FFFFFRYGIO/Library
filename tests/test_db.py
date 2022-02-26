from sqlalchemy import update, delete

from db_connect import db, session
from db_create_tables import Book

TEST_BOOK = {
    'ISBN': '1234567890123',
    'title': 'test title',
    'authors': 'test author',
    'publishedDate': '2022-02-24',
    'thumbnail': '<no thumbnail>',
    'pageCount': None,
    'language': '<no lan.>',
}


def test_tables():
    # if database contains only "book" table
    tables = db.table_names()
    assert tables == ['book']

    # if database can insert book
    curr_book = Book()
    curr_book.ISBN = TEST_BOOK['ISBN']
    curr_book.title = TEST_BOOK['title']
    curr_book.authors = TEST_BOOK['authors']
    curr_book.publishedDate = TEST_BOOK['publishedDate']
    curr_book.thumbnail = TEST_BOOK['thumbnail']
    curr_book.pageCount = TEST_BOOK['pageCount']
    curr_book.language = TEST_BOOK['language']
    session.add(curr_book)
    session.commit()

    # if inserted book is the same as input
    import_book = session.query(Book).filter(Book.ISBN == TEST_BOOK['ISBN']).first().__dict__
    for key in TEST_BOOK:
        assert import_book[key] == TEST_BOOK[key]

    # if database can update book
    upd_book = (update(Book).where(Book.ISBN == TEST_BOOK['ISBN']).values(pageCount=100))
    session.execute(upd_book)
    session.commit()
    import_pages = session.query(Book).filter(Book.ISBN == TEST_BOOK['ISBN']).first().__dict__['pageCount']
    assert import_pages == 100

    # if database can delete book
    del_book = (delete(Book).where(Book.ISBN == TEST_BOOK['ISBN']))
    session.execute(del_book)
    session.commit()
    import_book = session.query(Book).filter(Book.ISBN == TEST_BOOK['ISBN']).first()
    assert import_book is None

