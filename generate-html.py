import base64
import os
from collections import defaultdict, namedtuple


import jinja2


from model import Book, Cover, book_to_cover, load_books


BookWithCover = namedtuple(
    'Book',
    list(Book._fields) + ['cover']
)


def render_from_template(template_filename, books_with_cover_by_year, pages_per_day):
    path, filename = os.path.split(template_filename)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(books_by_year=books_with_cover_by_year, pages_per_day=pages_per_day)


def get_inline_image(filename):
    _, file_extension = os.path.splitext(filename)
    with open(filename, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')
    return "data:image/%s;base64,%s" % (file_extension, encoded_string)


def main(input_filename, cover_directory, output_directory):
    books = load_books(input_filename)
    books_with_cover_by_year = defaultdict(list)
    pages_by_year= defaultdict(int)

    for book in books:
        cover = book_to_cover(book, cover_directory)
        cover_base64 = get_inline_image(cover.full_path)
        book_with_cover = BookWithCover(**book._asdict(), cover=cover_base64)

        year = book_with_cover.year_read
        year = "Earlier" if year == 0 else year

        pages_by_year[year] += book_with_cover.num_pages
        books_with_cover_by_year[year].append(book_with_cover._asdict())

    pages_per_day = {year: round(pages_by_year[year] / 365.25, 1) for year in pages_by_year.keys() if year != 'Earlier'}

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    output_filename = os.path.join(output_directory, 'reading.html')
    with open(output_filename, 'w') as f:
        output = render_from_template('templates/reading.html.j2', books_with_cover_by_year, pages_per_day)
        f.write(output)


if __name__ == '__main__':
    main(
        input_filename='goodreads.json',
        cover_directory='covers',
        output_directory='output'
    )
