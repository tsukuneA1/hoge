-- name: ListCourses :many
SELECT * FROM courses;

-- name: GetCourseByPkey :one
SELECT * FROM courses
WHERE pkey = $1;

-- name: UpsertCourses :exec
INSERT INTO courses
(
    pkey,
    academic_year,
    faculty, title,
    instructor,
    term_day_period,
    category,
    eligible_year,
    credits,
    classroom,
    campus,
    course_key,
    class_code,
    language,
    delivery_mode,
    course_code,
    field_large,
    field_middle,
    field_small,
    level,
    class_format,
    subtitle,
    overview,
    objectives,
    before_after_study,
    lesson_plan,
    textbook,
    reference_text,
    grading_policy,
    remarks,
    syllabus_updated_at,
    source_url,
    raw_html
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32, $33)
ON CONFLICT (pkey) DO UPDATE SET
academic_year = excluded.academic_year,
faculty = excluded.faculty,
title = excluded.title,
instructor = excluded.instructor,
term_day_period = excluded.term_day_period,
category = excluded.category,
eligible_year = excluded.eligible_year,
credits = excluded.credits,
classroom = excluded.classroom,
campus = excluded.campus,
course_key = excluded.course_key,
class_code = excluded.class_code,
language = excluded.language,
delivery_mode = excluded.delivery_mode,
course_code = excluded.course_code,
field_large = excluded.field_large,
field_middle = excluded.field_middle,
field_small = excluded.field_small,
level = excluded.level,
class_format = excluded.class_format,
subtitle = excluded.subtitle,
overview = excluded.overview,
objectives = excluded.objectives,
before_after_study = excluded.before_after_study,
lesson_plan = excluded.lesson_plan,
textbook = excluded.textbook,
reference_text = excluded.reference_text,
grading_policy = excluded.grading_policy,
remarks = excluded.remarks,
syllabus_updated_at = excluded.syllabus_updated_at,
source_url = excluded.source_url,
raw_html = excluded.raw_html,
updated_at = NOW();
