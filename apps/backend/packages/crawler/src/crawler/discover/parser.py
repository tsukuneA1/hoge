import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchPageParseResult:
    total_count: int
    pkeys: list[str]


PKEY_PATTERN = re.compile(r"post_submit\('JAA104DtlSubCon',\s*'(?P<pkey>[^']+)'\)")
TOTAL_COUNT_PATTERN = re.compile(r"全(?P<total>\d+)件中")


def extract_pkeys(html: str) -> list[str]:
    return list(
        dict.fromkeys(match.group("pkey") for match in PKEY_PATTERN.finditer(html))
    )


def extract_total_count(html: str) -> int:
    match = TOTAL_COUNT_PATTERN.search(html)
    if match is None:
        raise ValueError("total_count was not found")
    return int(match.group("total"))
