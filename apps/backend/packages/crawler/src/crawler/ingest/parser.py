from dataclasses import dataclass
from datetime import datetime
from logging import getLogger

from bs4 import BeautifulSoup

from crawler.ingest.normalize import clean_text

logger = getLogger(__name__)


@dataclass(frozen=True)
class ParsedCourse:
    academic_year: int
    faculty: str
    title: str
    instructor: str | None
    term_day_period: str
    # NOTE: 科目区分はnull許容
    category: str | None
    eligible_year: str
    credits: int
    # NOTE: 教室はnull許容
    classroom: str | None
    campus: str
    course_key: str
    class_code: str | None
    language: str
    # NOTE: 授業方法区分はnull許容
    delivery_mode: str | None
    course_code: str | None
    field_large: str
    field_middle: str
    field_small: str
    level: str
    class_format: str
    # NOTE: 副題はnull許容 (https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey=2600001002012026260000100226&pLng=jp)
    subtitle: str | None
    overview: str | None
    objectives: str
    before_after_study: str
    lesson_plan: str | None
    # NOTE: 教科書はnull許容 (https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey=1100001250012026110000125011&pLng=jp)
    textbook: str | None
    # NOTE: 参考文献はnull許容 (https://www.wsl.waseda.jp/syllabus/JAA104.php?pKey=1100001270012026110000127011&pLng=jp)
    reference_text: str | None
    grading_policy: str
    # NOTE: 備考関連URLはnull許容
    remarks: str
    syllabus_updated_at: datetime


def parse_course_detail(html: str) -> ParsedCourse:
    soup = BeautifulSoup(html, "lxml")

    academic_year = int(
        get_required_value_by_label(soup, "開講年度").replace("年度", "")
    )
    faculty = get_required_value_by_label(soup, "開講箇所")
    title = get_required_value_by_label(soup, "科目名")
    instructor = get_optional_value_by_label(soup, "担当教員")
    term_day_period = get_required_value_by_label(soup, "学期曜日時限")
    category = get_optional_value_by_label(soup, "科目区分")
    eligible_year = get_required_value_by_label(soup, "配当年次")
    credits = int(get_required_value_by_label(soup, "単位数"))
    classroom = get_optional_value_by_label(soup, "使用教室")
    campus = get_required_value_by_label(soup, "キャンパス")
    course_key = get_required_value_by_label(soup, "科目キー")
    class_code = get_optional_value_by_label(soup, "科目クラスコード")
    language = get_required_value_by_label(soup, "授業で使用する言語")
    delivery_mode = get_optional_value_by_label(soup, "授業方法区分")
    course_code = get_optional_value_by_label(soup, "コース・コード")
    field_large = get_required_value_by_label(soup, "大分野名称")
    field_middle = get_required_value_by_label(soup, "中分野名称")
    field_small = get_required_value_by_label(soup, "小分野名称")
    level = get_required_value_by_label(soup, "レベル")
    class_format = get_required_value_by_label(soup, "授業形態")
    subtitle = get_optional_value_by_label(soup, "副題")
    overview = get_optional_value_by_label(soup, "授業概要")
    objectives = get_required_value_by_label(soup, "授業の到達目標")
    before_after_study = get_required_value_by_label(soup, "事前・事後学習の内容")
    lesson_plan = get_optional_value_by_label(soup, "授業計画")
    textbook = get_optional_value_by_label(soup, "教科書")
    reference_text = get_optional_value_by_label(soup, "参考文献")
    grading_policy = get_required_value_by_label(soup, "成績評価方法")
    remarks = get_optional_value_by_label(soup, "備考・関連URL")
    syllabus_updated_at = get_last_updated_at(soup)

    return ParsedCourse(
        academic_year=academic_year,
        faculty=faculty,
        title=title,
        instructor=instructor,
        term_day_period=term_day_period,
        category=category,
        eligible_year=eligible_year,
        credits=credits,
        classroom=classroom,
        campus=campus,
        course_key=course_key,
        class_code=class_code,
        language=language,
        delivery_mode=delivery_mode,
        course_code=course_code,
        field_large=field_large,
        field_middle=field_middle,
        field_small=field_small,
        level=level,
        class_format=class_format,
        subtitle=subtitle,
        overview=overview,
        objectives=objectives,
        before_after_study=before_after_study,
        lesson_plan=lesson_plan,
        textbook=textbook,
        reference_text=reference_text,
        grading_policy=grading_policy,
        remarks=remarks,
        syllabus_updated_at=syllabus_updated_at,
    )


def get_required_value_by_label(soup: BeautifulSoup, label: str) -> str:
    value = get_optional_value_by_label(soup, label)
    if value is None or value == "":
        raise ValueError(f"required field not found: {label}")

    return value


def get_optional_value_by_label(soup: BeautifulSoup, label: str) -> str | None:
    label_cell = soup.find(
        ["th", "td"],
        string=lambda s: s is not None and s.strip() == label,
    )
    if label_cell is None:
        return None

    value_cell = label_cell.find_next_sibling(["td", "th"])
    if value_cell is None:
        return None

    return clean_text(value_cell.get_text(" ", strip=True))


def get_last_updated_at(soup: BeautifulSoup) -> datetime:
    h2 = soup.find("h2", string=lambda s: s is not None and "最終更新日時" in s)

    text = h2.get_text(strip=True).replace("最終更新日時：", "").strip()
    return datetime.strptime(text, "%Y/%m/%d %H:%M:%S")
