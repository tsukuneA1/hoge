-- name: ListCourses :many
SELECT * from courses;

-- name: GetSyllabusByPkey :one
SELECT * from courses
WHERE pkey = $1;

-- name: UpsertCourses :exec
INSERT INTO courses (pkey, academic_year, faculty, title, instructor, term_day_period, category, eligible_year, credits, classroom, campus, course_key, class_code, language)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, NOW())
ON CONFLICT (id) DO UPDATE SET
    academic_year        = EXCLUDED.academic_year,
    faculty    = EXCLUDED.faculty,
    title = EXCLUDED.title,
    instructor = EXCLUDED.instructor,
    term_day_period = EXCLUDED.term_day_period,
    category = EXCLUDED.category,
    eligible_year = EXCLUDED.eligible_year,
    credits = EXCLUDED.credits,
    classroom = EXCLUDED.classroom,
    campus = EXCLUDED.campus,
    course_key = EXCLUDED.course_key,
    class_code = EXCLUDED.class_code,
    language = EXCLUDED.language,
    updated_at   = NOW();
