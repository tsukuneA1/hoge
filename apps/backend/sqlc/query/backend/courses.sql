-- name: ListCourses :many
SELECT * FROM courses;

-- name: GetCourseByPkey :one
SELECT * FROM courses
WHERE pkey = $1;

-- name: UpsertCourses :exec
INSERT INTO courses (pkey, academic_year, faculty, title, instructor, term_day_period, category, eligible_year, credits, classroom, campus, course_key, class_code, language)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, NOW())
ON CONFLICT (id) DO UPDATE SET
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
updated_at = NOW();
