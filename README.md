
# Laptop_Scraper
This tool allows semi automatic scraping of laptop offers on eBay

## Getting started
- Follow the link below to the eBay research site which lists offers currently online on eBay (requires eBay account). Set the desired price range with `min_price`, `max_price`. Adjust `offset` and `limit` to get a different portion of the data e.g. offset=50 limit=50 gives the 2nd page with 50 entries. Setting `limit` higher than 1000 might result in poor performance or the browser crashing. Currently the parser is expecting the German version of the site.
- Download the site and move it to `/input_data`, supported file types:
  - Firefox: `.txt` (fastest) / `.htm` (full site)
  - Edge, Chrome: `.html` (full site)
- run `pip install -r requirements.txt`
- run `src/main.py`

Link to download site:
https://www.ebay.de/sh/research?marketplace=EBAY-DE&keywords=Laptop&dayRange=90&endDate=1733260222746&startDate=1725480622746&categoryId=0&format=FIXED_PRICE&minPrice=80&maxPrice=400&offset=0&limit=100&tabName=ACTIVE&tz=Europe%2FBerlin

## How it works
Laptop_Scraper will extract the item IDs out of all files in `/input_data` and scrape the corresponding offers. It will then create a database including:
- Name
- Price
- RAM size
- Disk size
- CPU
- CPU Bench score (https://www.cpubenchmark.net/CPU_mega_page.html)

It then launches a GUI with a price/CPU-score chart which makes it easy to find good offers. Remember the chart will not be complete as not all offers include the CPU name in a format the parser can detect.

## QoL

On launch Laptop_Scraper will re-scrape database entries older than one day to keep the database up to date, offers which are not available anymore will get marked as offline and not be included in the chart. There is a button to include historical data if needed.

You also dont have to remove old files in `/input_data` as URLs will be ignored if they are already in the database.