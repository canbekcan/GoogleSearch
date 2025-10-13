# This version does not work anymore due to Google Search page structure changes.

import requests
from parsel import Selector
import csv
from datetime import datetime

# Define the base URL for Google News
# BASE_URL = "https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en"
BASE_URL = "https://news.google.com/search?q={query}&hl=tr&gl=TR&ceid=TR:tr"

# Define the search query
SEARCH_QUERY = input("Search terms: ")

# Define the CSV output file
OUTPUT_FILE = input("Enter the filename for the CSV (without extension): ") + ".csv"

def scrape_google_news(query, pages=1):
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Source", "Date"])

        for page in range(pages):
            # Generate the URL for the current page
            url = BASE_URL.format(query=query)
            response = requests.get(url)

            print(f"Response status code: {response.status_code}")

            if response.status_code != 200:
                print(f"Failed to fetch page {page + 1}: HTTP {response.status_code}")
                continue

            # Parse the HTML content
            html = response.text
            selector = Selector(text=html)

            print(f"Page {page + 1}:")
            print('--------------------------')

            # Loop through each article container
            for article in selector.css('article'):
                # Extract source
                source = article.css('div.vr1PYe::text').get()

                # Extract title
                title = article.css('a.JtKRv::text').get()

                # Extract link
                link = article.css('a.JtKRv::attr(href)').get()
                if link and not link.startswith("http"):
                    link = f"https://news.google.com{link[1:]}"  # Fix relative links

                # Extract and format date
                raw_date = article.css('time::attr(datetime)').get()
                if raw_date:
                    try:
                        # Convert the ISO-8601 format into a readable date
                        date = datetime.fromisoformat(raw_date.rstrip('Z')).strftime('%d %B %Y %H:%M:%S')
                    except ValueError:
                        date = "Invalid Date"
                else:
                    date = "Unknown"

                if title and link:
                    # Write data to the CSV file
                    writer.writerow([
                        title.strip(),
                        link.strip(),
                        source.strip() if source else "Unknown",
                        date
                    ])

                    # Print the data (optional)
                    print(f"Title: {title}")
                    print(f"Link: {link}")
                    print(f"Source: {source}")
                    print(f"Date: {date}")
                    print('--------------------------')

if __name__ == "__main__":
    scrape_google_news(SEARCH_QUERY, pages=1)

