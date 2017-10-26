# goodreads-scraper
:book: Scrape Goodreads RSS feed

Render a static HTML page for your Goodreads books per year, with average pages read per day. You can view an example [here](https://niklaslindblad.se/reading).

## Usage

    virtualenv -p python3 venv
    python scrape.py 'https://www.goodreads.com/review/list_rss/12625940?key=XXX&shelf=read'
    python download-covers.py
    python generate-html.py
    cp output/reading.html somewhere

## Result

[![Reading summary](https://cdn.niklaslindblad.se/images/reading.png)](https://niklaslindblad.se/reading)
