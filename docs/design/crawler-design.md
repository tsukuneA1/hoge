# 設計ドキュメント: Crawler Strategy

## 概要

早稲田大学シラバスサイト (`wsl.waseda.jp/syllabus/`) からシラバスデータを収集するクローラーの設計。
`nendo` パラメータのみで全学部・全学科のシラバスを一括取得する。

## 目標

- **主要な目標**
  - `JAA103.php?nendo={year}` から全シラバスのidを収集する
  - id一覧をもとに `JAA104.php` から詳細データを取得してDBに保存する
  - サイトに不必要な負荷をかけないレート制限を実装する

- **非目標**
  - リアルタイムクローリング（定期バッチ実行を想定）
  - ログイン後のコンテンツ取得（公開シラバスのみ対象）
  - 全年度データの常時最新化（年度単位での更新を想定）

## 背景

早稲田大学のシラバスシステムは以下の3ページで構成される：

```
JAA101.php  検索条件入力
    ↓
JAA103.php  検索結果一覧（JavaScriptで動的生成）
    ↓
JAA104.php?id=XXXX  シラバス詳細
```

シラバス詳細ページ（JAA104.php）は28文字の `id` パラメータで一意に識別される。
idが判明すれば直接アクセスが可能。検索結果ページのリンクはJavaScript動的生成のため、
静的HTMLスクレイピングではidを取得できない。

`JAA103.php` のGETパラメータのうち `nendo` のみが有効に機能する。
2026年度の全シラバスは約35,000件。

## 設計

### アーキテクチャ

```
PlaywrightSearcher
  └── JAA103.php?nendo={year} → ページネーション全走査 → id一覧
          ↓
      httpx (逐次, 1req/s)
          ↓
      JAA104.php?id=XXXX → SyllabusParser
          ↓
      PostgreSQL (syllabuses テーブル)
```

### クローリング戦略

`JAA103.php?pLng=jp&nendo={year}` に対してPlaywrightでアクセスし、
ページネーションを全走査してidを収集する。

```python
async def fetch_all_ids(page: Page, nendo: str) -> list[str]:
    url = f"https://www.wsl.waseda.jp/syllabus/JAA103.php?pLng=jp&nendo={nendo}"
    await page.goto(url)
    await page.wait_for_load_state("networkidle")

    ids = []
    while True:
        links = await page.query_selector_all("a[href*='JAA104.php']")
        for link in links:
            href = await link.get_attribute("href")
            id = extract_id_from_href(href)
            if id:
                ids.append(id)

        # 次ページへ（なければ終了）
        next_btn = await page.query_selector("次ページのセレクタ")
        if not next_btn:
            break
        await next_btn.click()
        await page.wait_for_load_state("networkidle")

    return ids
```

#### 動作確認済みパラメータ

| パラメータ | 効果 | 例 |
|-----------|------|----|
| `pLng` | 言語切替 | `jp` |
| `nendo` | 年度で絞り込み ✅ | `2026` |
| `p_gakubu` | 学部で絞り込み ✅ | `51`（基幹理工）|
| `p_nendo` | 効かない | - |
| `p_keyw` | 効かない（POSTのみ） | - |

### Playwright / httpx の使い分け

| 用途 | ツール | 理由 |
|------|--------|------|
| 検索結果ページのid収集（JAA103.php） | `Playwright` | JavaScriptでリンク動的生成 |
| シラバス詳細取得（JAA104.php） | `httpx` | JavaScript不要、静的HTML |

### id構造（参考）

idは**28文字固定**。基幹理工学部は数字のみ、他学部は英数字混在のケースあり。

```
位置   文字数  内容
1-2    2       年度下2桁
3-4    2       学科コード
5-6    2       科目区分コード
7-10   4       科目コード（学年+連番）
11-12  2       クラスコード
13-16  4       開講年度（4桁）
17-28  12      参照先情報（通常は前半の繰り返し）
```

idはJAA103.phpから取得するため、構造の詳細知識はクローラーの動作に不要。

### HTMLパース戦略

```python
from bs4 import BeautifulSoup

def parse_syllabus(html: str, id: str) -> dict | None:
    soup = BeautifulSoup(html, "html.parser")

    if is_error_page(soup):
        return None

    return {
        "id": id,
        "title": extract_title(soup),
        "instructor": extract_instructor(soup),
        "semester": extract_semester(soup),
        "credits": extract_credits(soup),
        "department": extract_department(soup),
        "year": extract_year(soup),
        "description": extract_description(soup),
        "objectives": extract_objectives(soup),
        "schedule": extract_schedule(soup),
        "evaluation": extract_evaluation(soup),
        "textbooks": extract_textbooks(soup),
        "raw_html": html,
    }
```

#### 学期情報の抽出

idに学期情報は含まれないため、シラバス本文から判定する：

```python
SEMESTER_KEYWORDS = {
    "spring": ["春学期", "Spring", "前期"],
    "fall":   ["秋学期", "Fall", "後期"],
    "full":   ["通年", "Full Year", "春学期・秋学期"],
}
```

### エラーハンドリングとリトライロジック

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def fetch_syllabus(client: httpx.AsyncClient, id: str) -> str | None:
    url = f"https://www.wsl.waseda.jp/syllabus/JAA104.php?id={id}&pLng=jp"
    try:
        resp = await client.get(url, timeout=30.0)
        resp.raise_for_status()
        return resp.text
    except httpx.TimeoutException:
        raise  # tenacityがリトライ
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise
```

| エラー | 対処 |
|--------|------|
| 404 | スキップ |
| タイムアウト | 最大3回リトライ（指数バックオフ） |
| 5xx | 最大3回リトライ後、警告ログ出力してスキップ |
| パースエラー | raw_htmlを保存してスキップ、後続処理は継続 |
| ネットワーク断 | リトライ後も失敗したら全体停止してチェックポイントを保存 |

### レート制限対策

```python
class RateLimitedCrawler:
    def __init__(self, requests_per_second: float = 1.0):
        self.interval = 1.0 / requests_per_second
        self._last_request_time = 0.0

    async def wait(self):
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request_time
        if elapsed < self.interval:
            await asyncio.sleep(self.interval - elapsed)
        self._last_request_time = asyncio.get_event_loop().time()
```

| 項目 | 値 |
|------|-----|
| リクエスト間隔 | 1秒以上 |
| 並列リクエスト数 | 1（逐次処理） |
| User-Agent | `WasedaSyllabusMCP/1.0 (research purpose)` |
| タイムアウト | 30秒 |

35,000件 × 1秒 ≒ 約10時間。年1回の定期実行を想定。

### チェックポイントと再開

```python
class CrawlState:
    def __init__(self, checkpoint_path: Path):
        self.checkpoint_path = checkpoint_path
        self.completed: set[str] = self._load()

    def mark_done(self, id: str):
        self.completed.add(id)
        if len(self.completed) % 100 == 0:
            self._save()

    def is_done(self, id: str) -> bool:
        return id in self.completed
```

### データ検証とクリーニング

```python
from pydantic import BaseModel, validator

class SyllabusRecord(BaseModel):
    id: str
    title: str
    instructor: str | None
    semester: Literal["spring", "fall", "full", "unknown"]
    credits: int | None
    year: int
    department: str

    @validator("id")
    def validate_id(cls, v):
        if len(v) != 28:
            raise ValueError(f"idは28文字必須: {v!r}")
        return v

    @validator("year")
    def validate_year(cls, v):
        if not (2000 <= v <= 2100):
            raise ValueError(f"年度が範囲外: {v}")
        return v
```

クリーニング処理：

- 全角スペース・改行の正規化
- タイトル前後の空白除去
- 教員名の重複除去（複数担当の場合）
- HTMLエンティティのデコード（`&amp;` → `&` 等）

### データモデル

```python
class Syllabus(Base):
    __tablename__ = "syllabuses"

    id = Column(String(28), primary_key=True)
    title = Column(String, nullable=False)
    instructor = Column(String)
    semester = Column(String(10))
    credits = Column(Integer)
    year = Column(Integer, nullable=False)
    department = Column(String)
    description = Column(Text)
    objectives = Column(Text)
    evaluation = Column(Text)
    raw_html = Column(Text)
    crawled_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
```

### 依存関係

- **httpx** - 非同期HTTPクライアント（シラバス詳細取得）
- **playwright** - ブラウザ自動化（検索結果ページのid収集）
- **beautifulsoup4** + **lxml** - HTMLパース
- **tenacity** - リトライロジック
- **pydantic** - データバリデーション
- **sqlalchemy[asyncio]** + **asyncpg** - DB保存

## 検討した代替案

| 案 | 採用しなかった理由 |
|---|---|
| id生成方式（基幹理工） | 存在しないidへの無駄なリクエストが発生、学部別コード管理が必要 |
| 学部コード（`p_gakubu`）でループ | `nendo`だけで全件取れるため不要 |
| Scrapy | asyncioとの統合が複雑、Playwrightとの連携が難しい |
| requests（同期） | 並列処理が困難、asyncioとの統合不可 |
| Selenium | Playwrightより低速・設定が煩雑 |

## 未解決の質問

- [ ] JAA103.php のページネーション構造（ページ送りのDOM操作方法）
- [ ] robots.txt の内容・スクレイピング可否（要確認）
- [ ] クローラー実行スケジューリング方式（cron vs GitHub Actions）

## テスト戦略

- **Unit テスト**: HTMLパーサー（モックHTMLを使用）
- **Integration テスト**: httpxのモックサーバーを立ててクローラー全体をテスト
- **Playwright テスト**: 静的HTMLファイルをローカルサーバーで配信してテスト
- **バリデーションテスト**: 不正なid・欠損フィールドに対するPydanticモデルの動作確認

## 参考資料

- [早稲田大学シラバス検索](https://www.wsl.waseda.jp/syllabus/JAA101.php)
- [Playwright Python ドキュメント](https://playwright.dev/python/)
- [httpx ドキュメント](https://www.python-httpx.org/)
- [tenacity ドキュメント](https://tenacity.readthedocs.io/)
- [BeautifulSoup4 ドキュメント](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
