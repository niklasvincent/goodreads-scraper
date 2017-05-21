# goodreads-scraper
:book: Scrape Goodreads RSS feed

## Usage

    virtualenv -p python3 venv
    python scrape.py 'https://www.goodreads.com/review/list_rss/12625940?key=XXX&shelf=read'
    python download-covers.py
    python generate-html.py
    cp output/reading.html somewhere
