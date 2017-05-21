import os
import urllib.request


from model import book_to_cover, load_books


def download_cover(cover):
    response = urllib.request.urlopen(cover.url)
    with open(cover.full_path, 'wb') as f:
        f.write(response.read())


def cover_exists(cover):
    return os.path.exists(cover.full_path)


def main(input_filename, output_directory):
    books = load_books(input_filename)
    covers = [book_to_cover(book, output_directory) for book in books]

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    for cover in covers:
        if not cover_exists(cover):
            download_cover(cover)


if __name__ == '__main__':
    main(
        input_filename='goodreads.json',
        output_directory='covers'
    )
