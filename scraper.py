import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    print(f"Scraping {url}...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])
        if not text:
            text = soup.get_text(separator=" ", strip=True)
        title = soup.find("title")
        title_text = title.get_text().strip() if title else url
        print(f"Scraped {len(text)} characters from {title_text}")
        return {"title": title_text, "url": url, "content": text, "char_count": len(text)}
    except Exception as e:
        return {"error": str(e), "url": url, "content": "", "char_count": 0}