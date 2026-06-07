from __future__ import annotations

import re
from pathlib import Path

import httpx

BASE_URL = "https://www.wsl.waseda.jp/syllabus"
YEAR = 2026
PAGE_SIZE = 2000
PAGES = [1, 2]

OUTPUT_DIR = Path(__file__).parent / "output"

PKEY_RE = re.compile(r"post_submit\('JAA104DtlSubCon', \s*'([^']+)'\)")
TOTAL_RE = re.compile(r"全(\d+)件中(\d+)件～(\d+)件を表示")

def build_form_data(*, year: int, page_size: int, page: int) -> dict[str, str]:
    return {
        "ControllerParameters" : "JAA103SubCon",
        "nendo": str(year),
        "pYear": str(year),
        "p_number": str(page_size),
        "p_page": str(page),
        "pLng": "jp",
    }

def as_multipart(data: dict[str, str]) -> dict[str, tuple[None, str]]:
    return {key: (None, value) for key, value in data.items()}

def extract_pkeys(html: str) -> list[str]:
    return PKEY_RE.findall(html)

def extract_total_line(html: str) -> str | None:
    text = re.sub(r"\s+", "", html)
    match = TOTAL_RE.search(text)
    if match is None:
        return None
    
    total, start, end = match.groups()
    return f"全{total}件中{start}件~{end}件を表示"

def fetch_search_page(
    client: httpx.Client,
    *,
    year: int,
    page_size: int,
    page: int,
) -> str:
    response = client.post(
        f"{BASE_URL}/JAA101.php",
        files=as_multipart(
            build_form_data(
                year=year,
                page_size=page_size,
                page=page,
            )
        ),
    )
    response.raise_for_status()
    return response.text

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with httpx.Client(follow_redirects=True, timeout=60.0) as client:
        for page in PAGES:
            html = fetch_search_page(
                client,
                year=YEAR,
                page_size=PAGE_SIZE,
                page=page,
            )

            output_path = OUTPUT_DIR / f"search_{YEAR}_page{page}_size{PAGE_SIZE}.html"
            output_path.write_text(html, encoding="utf-8")

            pkeys = extract_pkeys(html)
            total_line = extract_total_line(html)

            print(f"saved: {output_path}")
            print(f"page={page}")
            print(f"total_line={total_line}")
            print(f"pkey_count={len(pkeys)}")
            print(f"first_pkey={pkeys[0] if pkeys else None}")
            print()


if __name__ == "__main__":
    main()
