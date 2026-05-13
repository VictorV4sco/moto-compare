from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def fetch_html_with_browser(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page(locale="pt-BR")

        page.goto("https://www.honda.com.br/motos/modelos", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)
        html = page.content()

        with open("debug_honda.html", "w", encoding="utf-8") as file:
            file.write(html)

        browser.close()
        return html

def get_internal_links(base_url: str, allowed_domains: list[str]) -> list[str]:
    html = fetch_html_with_browser(base_url)

    soup = BeautifulSoup(html, "lxml")
    links = set()

    for tag in soup.find_all("a", href=True):
        full_url = urljoin(base_url, tag["href"])
        parsed = urlparse(full_url)

        if parsed.netloc in allowed_domains:
            links.add(full_url.split("#")[0])

    return sorted(links)


def filter_possible_model_links(links: list[str]) -> list[str]:
    ignored_paths = [
        "/atendimento",
        "/blog",
        "/concessionarias",
        "/harmonia-no-transito",
        "/honda-store",
        "/modelos",
        "/tenho-interesse",
        "/pos-venda",
    ]

    valid_categories = [
        "/motos/adventure/",
        "/motos/off-road/",
        "/motos/sport/",
        "/motos/street/",
        "/motos/touring/",
    ]

    filtered_links = []

    for link in links:
        lower_link = link.lower()

        if any(path in lower_link for path in ignored_paths):
            continue

        if any(category in lower_link for category in valid_categories):
            filtered_links.append(link)

    return filtered_links