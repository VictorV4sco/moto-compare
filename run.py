from app.brands import BRANDS
from app.crawler import (
    fetch_html_with_browser,
    get_internal_links,
    filter_possible_model_links,
)
from app.extractors.honda import extract_honda_catalog
from app.finder import find_best_model_url


brand = BRANDS["honda"]

links = get_internal_links(
    base_url=brand["base_url"],
    allowed_domains=brand["allowed_domains"],
    headless=brand.get("headless", True),
)

model_links = filter_possible_model_links(links)

html = fetch_html_with_browser(
    brand["base_url"],
    headless=brand.get("headless", True),
)

catalog = extract_honda_catalog(html, brand["base_url"])

for item in catalog:
    item["model_url"] = find_best_model_url(
        item["model"],
        model_links,
    )

for item in catalog:
    print(item)