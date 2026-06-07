import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.wsl.waseda.jp/syllabus/JAA103.php?nendo=2026")
    page.get_by_role("link", name="次へ>").click()
    page.get_by_role("link", name="次へ>").click()
    page.get_by_role("link", name="次へ>").click()
    page.get_by_role("columnheader", name="科目名").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="基礎演習 ４０").click()
    page1 = page1_info.value
    page1.get_by_role("cell", name="年度").click()
    page1.get_by_role("cell", name="政治経済学部", exact=True).click()
    page1.get_by_role("rowheader", name="開講年度").click()
    page1.get_by_role("rowheader", name="開講箇所").click()
    page1.get_by_role("rowheader", name="科目名").click()
    page1.get_by_role("rowheader", name="担当教員").click()
    page1.get_by_role("rowheader", name="学期曜日時限").click()
    page1.get_by_role("rowheader", name="科目区分").click()
    page1.get_by_role("rowheader", name="配当年次").click()
    page1.get_by_role("rowheader", name="単位数").click()
    page1.get_by_role("rowheader", name="使用教室").click()
    page1.get_by_role("rowheader", name="キャンパス").click()
    page1.get_by_role("rowheader", name="科目キー").click()
    page1.get_by_role("rowheader", name="科目クラスコード").click()
    page1.get_by_role("rowheader", name="授業で使用する言語").click()
    page1.get_by_role("rowheader", name="授業方法区分").click()
    page1.get_by_role("rowheader", name="コース・コード").click()
    page1.get_by_role("rowheader", name="大分野名称").click()
    page1.get_by_role("rowheader", name="中分野名称").click()
    page1.get_by_role("rowheader", name="小分野名称").click()
    page1.get_by_role("rowheader", name="レベル").click()
    page1.get_by_role("rowheader", name="授業形態").click()
    page1.get_by_role("rowheader", name="副題").click()
    page1.get_by_role("rowheader", name="授業概要").click()
    page1.get_by_role("rowheader", name="授業の到達目標").click()
    page1.get_by_role("rowheader", name="事前・事後学習の内容").click()
    page1.get_by_role("rowheader", name="授業計画").click()
    page1.get_by_role("rowheader", name="教科書").click()
    page1.get_by_role("rowheader", name="参考文献").click()
    page1.get_by_role("rowheader", name="成績評価方法").click()
    page1.get_by_role("rowheader", name="備考・関連URL").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
