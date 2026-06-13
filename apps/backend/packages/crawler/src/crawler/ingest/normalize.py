import unicodedata


def clean_text(value: str) -> str:
    value = " ".join(value.replace("\xa0", " ").replace("\u3000", " ").split())
    value = unicodedata.normalize("NFKC", value)
    return " ".join(value.split())
