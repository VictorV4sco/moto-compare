from app.crawler import fetch_html_with_browser
from app.extractors.honda import extract_honda_catalog


url = "https://www.honda.com.br/motos/modelos"

html = fetch_html_with_browser(url, headless=False)

catalog = extract_honda_catalog(html, url)

for item in catalog:
    print(item)