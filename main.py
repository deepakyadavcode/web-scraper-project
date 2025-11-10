import requests
from bs4 import BeautifulSoup
import time

# --- Configuration ---
# Target URL: Using a publicly available site designed for scraping tutorials
TARGET_URL = "http://quotes.toscrape.com/"

def scrape_quotes_and_authors(url):
    """
    Connects to the specified URL, extracts quote text and author names,
    and prints the results.

    Args:
        url (str): The URL of the page to scrape.
    """
    print(f"--- Starting Scraper: Target URL is {url} ---")

    # 1. Fetch the HTML content
    try:
        # Use requests.get to download the page content
        response = requests.get(url, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    # 2. Parse the HTML content using BeautifulSoup
    # 'html.parser' is Python's built-in parser
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. Find the main containers for the data
    # The quotes are contained within <div> elements with the class "quote"
    quote_elements = soup.find_all('div', class_='quote')

    # Check if any quotes were found
    if not quote_elements:
        print("No quote elements found on the page. Check the website's structure.")
        return

    extracted_data = []

    # 4. Iterate over each container to extract specific details
    for quote_element in quote_elements:

        # Extract the quote text:
        # It's inside a <span class="text"> tag within the quote container
        quote_text_tag = quote_element.find('span', class_='text')
        quote_text = quote_text_tag.get_text(strip=True) if quote_text_tag else "N/A"

        # Extract the author name:
        # It's inside a <small class="author"> tag within the quote container
        author_tag = quote_element.find('small', class_='author')
        author_name = author_tag.get_text(strip=True) if author_tag else "N/A"

        # Extract tags:
        # Tags are inside a <div class="tags"> and then multiple <a class="tag">
        tag_list = quote_element.find('div', class_='tags')
        tags = [a.get_text(strip=True) for a in tag_list.find_all('a', class_='tag')] if tag_list else []


        extracted_data.append({
            "quote": quote_text,
            "author": author_name,
            "tags": tags
        })

    # 5. Output the extracted data
    print(f"\nSuccessfully scraped {len(extracted_data)} quotes from the page:\n")
    for i, item in enumerate(extracted_data, 1):
        print(f"--- Quote {i} ---")
        print(f"Quote:   {item['quote']}")
        print(f"Author:  {item['author']}")
        print(f"Tags:    {', '.join(item['tags'])}\n")

    print("--- Scraping Complete ---")


if __name__ == "__main__":
    # In a real application, you should add a small delay (e.g., time.sleep(1))
    # between requests to be polite to the server and avoid being blocked.
    scrape_quotes_and_authors(TARGET_URL)

    # Note: To handle multiple pages (pagination), you would typically:
    # 1. Find the "Next Page" link (e.g., <li class="next"><a href="/page/2/">Next</a></li>)
    # 2. Extract the relative URL (e.g., "/page/2/")
    # 3. Construct the new absolute URL
    # 4. Loop the scrape function with the new URL until the link is not found.