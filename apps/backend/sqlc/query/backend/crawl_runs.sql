-- name: ListCrawlRunsByStatus :many
SELECT *
FROM crawl_runs
WHERE status = @status
ORDER BY started_at DESC
LIMIT @row_limit;

-- name: CreateCrawlRun :exec
INSERT INTO crawl_runs (
    job_type,
    status,
    started_at
)
VALUES (
    @job_type,
    'running',
    now()
)
RETURNING *;

-- name: FinishCrawlRun :exec
UPDATE crawl_runs
SET
    status = @status,
    finished_at = now(),
    discovered_count = @discovered_count,
    ingested_count = @ingested_count,
    failed_count = @failed_count,
    error_message = @error_message
WHERE id = @id
RETURNING *;

-- name: GetCrawlRun :one
SELECT * FROM crawl_runs WHERE id = @id;
