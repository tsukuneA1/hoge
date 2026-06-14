-- name: ListIngestTargets :many
SELECT * 
FROM crawl_targets
WHERE
    status = 'pending'
    OR (status = 'failed' AND attempts < @max_attempts)
    OR (
        status = 'running'
        AND updated_at < now() - make_interval(secs => @lease_timeout_seconds)
    )
ORDER BY
    last_ingested_at NULLS FIRST,
    updated_at ASC
LIMIT @row_limit;

-- name: UpsertCrawlTarget :one
INSERT INTO crawl_targets (
    pkey,
    last_seen_run_id,
    status,
    discovered_year,
    source_page,
    first_discovered_at,
    last_discovered_at,
    created_at,
    updated_at
)
VALUES (
    @pkey,
    @last_seen_run_id,
    'pending',
    @discovered_year,
    @source_page,
    now(),
    now(),
    now(),
    now()
)
ON CONFLICT (pkey)
DO UPDATE SET
    last_seen_run_id = EXCLUDED.last_seen_run_id,
    discovered_year = EXCLUDED.discovered_year,
    source_page = EXCLUDED.discovered_year,
    last_discovered_at = now(),
    updated_at = now()
RETURNING *;

-- name: MarkCrawlTargetRunning :one
UPDATE crawl_targets
SET
    status = 'running',
    attempts = attempts + 1,
    last_error = NULL,
    updated_at = now()
WHERE pkey = @pkey
RETURNING *;

-- name: MarkCrawlTargetSucceeded :one
UPDATE crawl_targets
SET
    status = 'succeeded',
    last_error = NULL,
    updated_at = now()
WHERE pkey = @pkey
RETURNING *;

-- name: MarkCrawlTargetFailed :one
UPDATE crawl_targets
SET
    status = 'failed',
    last_error = @last_error,
    updated_at = now()
WHERE pkey = @pkey
RETURNING *;
