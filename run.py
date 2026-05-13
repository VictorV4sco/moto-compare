from app.brands import BRANDS
from app.crawler import get_internal_links, filter_possible_model_links


brand = BRANDS["honda"]

links = get_internal_links(
    base_url=brand["base_url"],
    allowed_domains=brand["allowed_domains"],
)

model_links = filter_possible_model_links(links)

print(f"Links encontrados: {len(links)}")
print(f"Possíveis modelos: {len(model_links)}")

for link in model_links:
    print(link)