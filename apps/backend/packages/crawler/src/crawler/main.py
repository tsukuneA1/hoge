from __future__ import annotations

from playwright.sync_api import BrowserContext, Page, Playwright, Request, Response, sync_playwright


TOP_URL = "https://www.wsl.waseda.jp/syllabus/JAA101.php"


def log_request(request: Request) -> None:
    """Network request logger.

    context.on("request") に付けることで、popup/new page側のrequestも拾いやすくする。
    """
    if "wsl.waseda.jp/syllabus" not in request.url:
        return

    print("\n=== REQUEST ===")
    print(request.method, request.url)

    if request.post_data:
        print("--- POST DATA ---")
        print(request.post_data)


def log_response(response: Response) -> None:
    """Network response logger."""
    if "wsl.waseda.jp/syllabus" not in response.url:
        return

    print("\n=== RESPONSE ===")
    print(response.status, response.url)


def attach_context_loggers(context: BrowserContext) -> None:
    """BrowserContext全体にloggerを付ける。

    page.on("request") だとpopup側を拾えないことがあるので、
    contextに付ける。
    """
    context.on("request", log_request)
    context.on("response", log_response)

    def on_page(page: Page) -> None:
        print("\n=== NEW PAGE ===")
        print(page.url)
        attach_page_loggers(page, page_name="popup-or-new-page")

    context.on("page", on_page)


def attach_page_loggers(page: Page, page_name: str) -> None:
    """Page単位のconsole/dialog logger."""
    page.on("console", lambda msg: print(f"BROWSER[{page_name}]:", msg.text))
    page.on("dialog", lambda dialog: handle_dialog(dialog))


def handle_dialog(dialog) -> None:
    """alertが出たら表示して閉じる。"""
    print("\n=== DIALOG ===")
    print(dialog.type, dialog.message)
    dialog.accept()


def install_form_submit_debugger(page: Page) -> None:
    """form.submit() を monkey patch して、submit直前のFormDataを見る。

    このサイトは document.cForm.submit() を直接呼んでいるっぽいので、
    addEventListener("submit") だけでは拾えない可能性がある。
    """
    page.evaluate(
        """
        () => {
          if (window.__crawlerSubmitPatched) {
            return;
          }
          window.__crawlerSubmitPatched = true;

          const originalSubmit = HTMLFormElement.prototype.submit;

          HTMLFormElement.prototype.submit = function() {
            console.log("=== FORM SUBMIT PATCHED ===");
            console.log("action=" + this.action);
            console.log("method=" + this.method);
            console.log("target=" + this.target);

            const fd = new FormData(this);
            for (const [key, value] of fd.entries()) {
              console.log(key + "=" + value);
            }

            return originalSubmit.call(this);
          };
        }
        """
    )


def install_function_debugger(page: Page) -> None:
    """func_submit / post_submit が呼ばれたら引数を出す。

    JSロード後に実行すること。
    """
    page.evaluate(
        """
        () => {
          if (window.__crawlerFunctionPatched) {
            return;
          }
          window.__crawlerFunctionPatched = true;

          if (typeof func_submit === "function") {
            const originalFuncSubmit = func_submit;
            window.func_submit = function(comma_string) {
              console.log("=== func_submit called ===");
              console.log("comma_string=" + comma_string);
              return originalFuncSubmit.call(this, comma_string);
            };
          } else {
            console.log("func_submit not found");
          }

          if (typeof post_submit === "function") {
            const originalPostSubmit = post_submit;
            window.post_submit = function(param) {
              console.log("=== post_submit called ===");
              console.log("param=" + param);
              return originalPostSubmit.call(this, param);
            };
          } else {
            console.log("post_submit not found");
          }
        }
        """
    )


def dump_submit_functions(page: Page) -> None:
    """func_submit / post_submit の関数定義を表示する。"""
    result = page.evaluate(
        """
        () => {
          return {
            func_submit: typeof func_submit === "function"
              ? func_submit.toString()
              : "func_submit not found",
            post_submit: typeof post_submit === "function"
              ? post_submit.toString()
              : "post_submit not found",
          };
        }
        """
    )

    print("\n=== func_submit ===")
    print(result["func_submit"])

    print("\n=== post_submit ===")
    print(result["post_submit"])


def dump_candidate_functions(page: Page) -> None:
    """window上のsubmit/JAA/pageっぽい関数名を出す。"""
    functions = page.evaluate(
        """
        () => Object.keys(window)
          .filter((key) => typeof window[key] === "function")
          .filter((key) =>
            key.toLowerCase().includes("submit") ||
            key.toLowerCase().includes("page") ||
            key.toLowerCase().includes("jaa") ||
            key.toLowerCase().includes("next") ||
            key.toLowerCase().includes("detail")
          )
          .sort()
        """
    )

    print("\n=== CANDIDATE FUNCTIONS ===")
    for name in functions:
        print(name)


def dump_form_inputs(page: Page, label: str) -> None:
    """form#cForm 内の input/select/textarea を出す。"""
    print(f"\n=== FORM INPUTS: {label} ===")

    elements = page.locator("form#cForm input, form#cForm select, form#cForm textarea")
    count = elements.count()

    for i in range(count):
        el = elements.nth(i)

        try:
            tag = el.evaluate("el => el.tagName.toLowerCase()")
            typ = el.get_attribute("type")
            name = el.get_attribute("name")
            element_id = el.get_attribute("id")

            # input_value() は input/select/textarea に使える
            try:
                value = el.input_value()
            except Exception:
                value = el.get_attribute("value")

            print(
                {
                    "tag": tag,
                    "type": typ,
                    "name": name,
                    "id": element_id,
                    "value": value,
                }
            )
        except Exception as e:
            print(f"failed to dump element {i}: {e}")


def dump_links(page: Page, label: str) -> None:
    """画面上のリンクをざっくり出す。詳細リンクや次へのonclickを見る用。"""
    print(f"\n=== LINKS: {label} ===")

    links = page.locator("a")
    count = links.count()

    for i in range(count):
        link = links.nth(i)
        try:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            onclick = link.get_attribute("onclick")

            if text or href or onclick:
                print(
                    {
                        "index": i,
                        "text": text,
                        "href": href,
                        "onclick": onclick,
                    }
                )
        except Exception as e:
            print(f"failed to dump link {i}: {e}")


def dump_buttons(page: Page, label: str) -> None:
    """button/input button/submit を出す。検索ボタンや次へボタンのonclickを見る用。"""
    print(f"\n=== BUTTONS: {label} ===")

    buttons = page.locator("button, input[type='button'], input[type='submit']")
    count = buttons.count()

    for i in range(count):
        button = buttons.nth(i)
        try:
            tag = button.evaluate("el => el.tagName.toLowerCase()")
            typ = button.get_attribute("type")
            name = button.get_attribute("name")
            value = button.get_attribute("value")
            onclick = button.get_attribute("onclick")
            text = button.inner_text().strip() if tag == "button" else ""

            print(
                {
                    "index": i,
                    "tag": tag,
                    "type": typ,
                    "name": name,
                    "value": value,
                    "text": text,
                    "onclick": onclick,
                }
            )
        except Exception as e:
            print(f"failed to dump button {i}: {e}")


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    context = browser.new_context()
    attach_context_loggers(context)

    page = context.new_page()
    attach_page_loggers(page, page_name="main")

    page.goto(TOP_URL)
    page.wait_for_load_state("domcontentloaded")

    # JSロード後にpatchする
    install_form_submit_debugger(page)
    install_function_debugger(page)

    # まず初期状態を全部見る
    dump_submit_functions(page)
    dump_candidate_functions(page)
    dump_form_inputs(page, "initial")
    dump_links(page, "initial")
    dump_buttons(page, "initial")

    print("\n=== READY ===")
    print("ブラウザで手動操作してください。")
    print("例: 学部条件を選ぶ → 検索 → 次へ → 科目リンククリック")
    print("操作中のrequest/form submit/function callがterminalに出るはずです。")
    input("操作が終わったらEnterで終了: ")

    # 手動操作後の状態も見る
    try:
        dump_form_inputs(page, "after manual operation")
        dump_links(page, "after manual operation")
        dump_buttons(page, "after manual operation")
    except Exception as e:
        print(f"failed to dump after operation: {e}")

    context.close()
    browser.close()


def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()