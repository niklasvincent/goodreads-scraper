import datetime
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict, OrderedDict


from model import Book


def fetch_file(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def parse_xml(xml):
    return ET.fromstring(xml)


def parse_date(string):
    if not string:
        return None
    return datetime.datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %z").date()


def extract_books(xml_root):
    def str2int(i):
        return 0 if not i else int(i)

    books = []
    for item in xml_root.iter('item'):
        title = item.find('title').text
        isbn = item.find('isbn').text
        author = item.find('author_name').text
        link = item.find('link').text
        num_pages = item.find('book').find('num_pages').text
        thumbnail_url = item.find('book_medium_image_url').text
        year_published = int(item.find('book_published').text)
        user_read_at = parse_date(item.find('user_read_at').text)
        user_read_at_year = user_read_at.year if user_read_at else 0
        books.append(Book(
            title=title,
            author=author,
            link=link,
            isbn=isbn,
            num_pages=str2int(num_pages),
            thumbnail_url=thumbnail_url,
            year_read=user_read_at_year,
            year_published=year_published
        ))
    return books


def main(goodreads_rss_url):
    xml_root = parse_xml(fetch_file(goodreads_rss_url))
    books = extract_books(xml_root)

    books_by_year = defaultdict(list)
    for book in books:
        books_by_year[book.year_read].append(book._asdict())
    books_by_year_sorted = OrderedDict(sorted(books_by_year.items(), reverse=True))

    with open('goodreads.json', 'w') as f:
        f.write(json.dumps(books_by_year_sorted))


if __name__ == '__main__':
    main(sys.argv[1])
