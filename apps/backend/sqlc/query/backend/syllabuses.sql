-- name: ListSyllabuses :many
SELECT * from syllabuses;

-- name: GetSyllabusById :one
SELECT * from syllabuses 
WHERE id = $1;

-- name: UpsertSyllabuses :exec
INSERT INTO syllabuses (id, title, title_en, year, semester, credits, department, instructors, description, objectives, schedule, evaluation, textbooks, crawled_at)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, NOW())
ON CONFLICT (id) DO UPDATE SET
    title        = EXCLUDED.title,
    title_en    = EXCLUDED.title_en,
    year = EXCLUDED.year,
    semester = EXCLUDED.semester,
    credits = EXCLUDED.credits,
    department = EXCLUDED.department,
    instructors  = EXCLUDED.instructors,
    description  = EXCLUDED.description,
    objectives   = EXCLUDED.objectives,
    schedule     = EXCLUDED.schedule,
    evaluation   = EXCLUDED.evaluation,
    textbooks    = EXCLUDED.textbooks,
    updated_at   = NOW();
