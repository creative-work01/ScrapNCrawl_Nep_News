#Assignment 1

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def analyze_website_link_structure(base_url, max_recursion_depth=1):
    """Analyzes the link structure of a website to determine its hub/authority characteristics.

    Args:
        base_url: The starting URL for the analysis.
        max_recursion_depth: The maximum depth to explore links (default: 1).

    Returns:
        None, but prints a conclusion about the website's role as a hub or authority.
    """

    processed_urls = set()  # Stores URLs that have already been visited
    internal_links = set()  # Stores URLs within the same domain
    external_links = set()  # Stores URLs linking to external domains
    unique_external_domains = set()  # Stores unique external domains linked to

    def explore_page(url, current_depth):
        if url in processed_urls or current_depth > max_recursion_depth:
            return

        processed_urls.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "lxml")

            for anchor_tag in soup.find_all("a", href=True):
                href = anchor_tag["href"]
                complete_url = urljoin(url, href)
                parsed_url = urlparse(complete_url)

                if parsed_url.netloc == urlparse(base_url).netloc:
                    internal_links.add(complete_url)
                    explore_page(complete_url, current_depth + 1)
                else:
                    external_links.add(complete_url)
                    unique_external_domains.add(parsed_url.netloc)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {url} ({e})")

            # Write collected URLs to files
        with open("processed_urls.txt", "w") as f:
            for url in processed_urls:
                f.write(url + "\n")

        with open("internal_links.txt", "w") as f:
            for url in internal_links:
                f.write(url + "\n")

        with open("external_links.txt", "w") as f:
            for url in external_links:
                f.write(url + "\n")

        with open("unique_external_domains.txt", "w") as f:
            for domain in unique_external_domains:
                f.write(domain + "\n")

    explore_page(base_url, 1)

    if len(unique_external_domains) >= len(internal_links):
        print("Website is likely a HUB, connecting to many external domains.")
    else:
        print("Website is likely an AUTHORITY, with a strong internal link structure.")

    

# scraping online khabar.com
starting_url = "https://www.onlinekhabar.com/"  
analyze_website_link_structure(starting_url, max_recursion_depth=2) 
