from __future__ import annotations

from pathlib import Path

import httpx


BASE_URL = "https://www.wsl.waseda.jp/syllabus"
P_KEY = "2600001002012026260000100226"

OUTPUT_DIR = Path(__file__).parent / "output"

def fetch_detail_page(client: httpx.Client, *, p_key: str) -> str:
    response = client.get(
        f"{BASE_URL}/JAA104.php",
        params={
            "pKey": p_key,
            "pLng": "jp",
        },
    )
    response.raise_for_status()
    return response.text

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with httpx.Client(follow_redirects=True, timeout=60.0) as client:
        html = fetch_detail_page(client, p_key=P_KEY)

    output_path = OUTPUT_DIR / f"detail_{P_KEY}.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"saved: {output_path}")
    print(f"bytes={len(html.encode('utf-8'))}")
    print("contains 授業情報:", "授業情報" in html)
    print("contains シラバス情報:", "シラバス情報" in html)


if __name__ == "__main__":
    main()
