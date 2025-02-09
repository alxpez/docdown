from curl_cffi import requests

session = requests.Session(impersonate="chrome")

def scrape_html(url):
    """Scrapes the HTML content of a given URL."""
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ [ERROR] scraping {url}:\n{e}")
        return None