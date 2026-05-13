import re
from rapidfuzz import fuzz, process


def normalize_name(text: str) -> str:
    text = text.lower()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = text.replace("/", " ")
    text = re.sub(r"([a-z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-z])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def url_to_candidate_name(url: str) -> str:
    slug = url.rstrip("/").split("/")[-1]
    return normalize_name(slug)


def find_best_model_url(model_name: str, urls: list[str]) -> str | None:
    candidates = {
        url_to_candidate_name(url): url
        for url in urls
    }

    normalized_model = normalize_name(model_name)

    match = process.extractOne(
        normalized_model,
        candidates.keys(),
        scorer=fuzz.token_sort_ratio,
    )

    if not match:
        return None

    candidate_name, score, _ = match

    if score < 55:
        return None

    return candidates[candidate_name]