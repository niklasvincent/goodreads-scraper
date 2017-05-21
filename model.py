import json
import os
from collections import namedtuple


Book = namedtuple(
    'Book',
    [
      'title',
      'author',
      'year_read',
      'year_published',
      'thumbnail_url',
      'link',
      'isbn',
      'num_pages'
    ]
)

Cover = namedtuple('Cover', ['full_path', 'url'])


def load_books(books_filename):
    with open(books_filename, 'r') as f:
        books = json.load(f)
    result = []
    for year in books.keys():
        for book in books[year]:
            result.append(Book(**book))
    return result


def book_to_cover(book, cover_directory):
    thumbnail_name = '_'.join(book.thumbnail_url.split('/')[-2:])
    return Cover(
        full_path=os.path.join(cover_directory, thumbnail_name),
        url=book.thumbnail_url
    )
