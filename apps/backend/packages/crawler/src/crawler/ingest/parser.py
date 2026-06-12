from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass(frozen=True)
class ParsedCourse:
    academic_year: str
    faculty: str
    title: str
    instructor: str
    term_day_period: str
    category: str
    eligible_year: str
    # credits: int
    # classroom: str
    # campus: str
    # course_key: str
    # class_code: str
    # language: str
    # delivery_mode: str
    # course_code: str
    # field_large: str
    # field_middle: str
    # field_small: str
    # level: str
    # class_format: str
    # subtitle: str
    # overview: str
    # objectives: str
    # before_after_study: str
    # lesson_plan: str
    # textbook: str
    # reference_text: str
    # grading_policy: str
    # remarks: str
    # syllabus_updated_at: str


def parse_course_detail(html: str) -> ParsedCourse:
    soup = BeautifulSoup(html, "lxml")

    academic_year = get_required_value_by_label(soup, "開講年度")
    faculty = get_required_value_by_label(soup, "開講箇所")
    title = get_required_value_by_label(soup, "科目名")
    instructor = get_required_value_by_label(soup, "担当教員")
    term_day_period = get_required_value_by_label(soup, "学期曜日時限")
    category = get_required_value_by_label(soup, "科目区分")
    eligible_year = get_required_value_by_label(soup, "配当年次")

    return ParsedCourse(
        academic_year=academic_year,
        faculty=faculty,
        title=title,
        instructor=instructor,
        term_day_period=term_day_period,
        category=category,
        eligible_year=eligible_year,
    )


def get_required_value_by_label(soup: BeautifulSoup, label: str) -> str:
    value = get_optional_value_by_label(soup, label)
    if value is None or value == "":
        raise ValueError()

    return value


def get_optional_value_by_label(soup: BeautifulSoup, label: str) -> str | None:
    label_cell = soup.find(["th", "td"], string=label)
    if label_cell is None:
        return None

    value_cell = label_cell.find_next_sibling(["td", "th"])
    if value_cell is None:
        return None

    return value_cell.get_text(" ", strip=True)
