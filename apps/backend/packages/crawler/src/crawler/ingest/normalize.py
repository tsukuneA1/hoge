import unicodedata


def clean_text(value: str) -> str:
    value = " ".join(value.replace("\xa0", " ").replace("\u3000", " ").split())
    return unicodedata.normalize("NFKC", value)
