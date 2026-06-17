import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchPageParseResult:
    total_count: int
    pkeys: list[str]


PKEY_PATTERN = re.compile(r"post_submit\('JAA104DtlSubCon',\s*'(?P<pkey>[^']+)'\)")
TOTAL_COUNT_PATTERN = re.compile(r"全(?P<total>\d+)件中")


def parse_search_page(html: str) -> SearchPageParseResult:
    total_count = extract_total_count(html)
    pkeys = extract_pkeys(html)

    return SearchPageParseResult(total_count=total_count, pkeys=pkeys)


def extract_pkeys(html: str) -> list[str]:
    return list(
        dict.fromkeys(match.group("pkey") for match in PKEY_PATTERN.finditer(html))
    )


def extract_total_count(html: str) -> int:
    match = TOTAL_COUNT_PATTERN.search(html)
    return int(match.group("total"))
