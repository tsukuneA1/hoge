CREATE TYPE crawl_job_type AS ENUM (
    'discover',
    'ingest'
);

CREATE TYPE crawl_run_status AS ENUM (
    'running',
    'succeeded',
    'partial_succeeded',
    'failed'
);

CREATE TYPE crawl_target_status AS ENUM (
    'pending',
    'running',
    'succeeded',
    'failed'
);

