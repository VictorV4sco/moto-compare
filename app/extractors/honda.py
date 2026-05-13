import re
from bs4 import BeautifulSoup


def parse_brl_price(text: str) -> float | None:
    match = re.search(r"R\$\s*([\d\.]+)", text)

    if not match:
        return None

    value = match.group(1).replace(".", "")
    return float(value)


def extract_honda_catalog(html: str, source_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    lines = soup.get_text("\n", strip=True).splitlines()

    results = []

    for index, line in enumerate(lines):
        current = line.strip()

        if current == "A partir de" and index > 0 and index + 1 < len(lines):
            model = lines[index - 1].strip()
            price_line = lines[index + 1].strip()
            price = parse_brl_price(price_line)

            if price:
                results.append(
                    {
                        "brand": "Honda",
                        "model": model,
                        "price_brl": price,
                        "source_url": source_url,
                    }
                )

    unique_results = {}

    for item in results:
        key = item["model"].lower()
        unique_results[key] = item

    return list(unique_results.values())