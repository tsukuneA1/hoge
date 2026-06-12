import re

PKEY_PATTERN = re.compile(r"post_submit\('JAA104DtlSubCon',\s*'(?P<pkey>[^']+)'\)")


def extract_pkeys(html: str) -> list[str]:
    return list(
        dict.fromkeys(match.group("pkey") for match in PKEY_PATTERN.finditer(html))
    )
