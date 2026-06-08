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

CREATE TABLE crawl_runs (
    id BIGSERIAL PRIMARY KEY,

    job_type crawl_job_type NOT NULL,
    status crawl_run_status NOT NULL,

    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at TIMESTAMPTZ,

    discovered_count INTEGER NOT NULL DEFAULT 0,
    ingested_count INTEGER NOT NULL DEFAULT 0,
    failed_count INTEGER NOT NULL DEFAULT 0,

    error_message TEXT
);

CREATE TABLE crawl_targets (
    pkey TEXT PRIMARY KEY,

    last_seen_run_id BIGSERIAL PREFERENCES crawl_runs(id),

    status crawl_target_status NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,

    discovered_year INTEGER NOT NULL,
    source_page INTEGER NOT NULL,

    first_discovered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_discovered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_ingested_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE courses (
    pkey TEXT PRIMARY KEY,
    -- 開講年度
    academic_year TEXT NOT NULL,
    -- 開講箇所(学部)
    faculty TEXT NOT NULL,
    -- 科目名
    title TEXT NOT NULL,
    -- 担当教員
    instructor TEXT NOT NULL,
    -- 学期曜日時限
    -- NOTE: カラムバラした方が良いカモ 「春学期  月３時限」みたいな感じで入っててパターンマッチでバラせそう 
    term_day_period TEXT NOT NULL,
    -- 科目区分 
    -- NOTE: ENUMに出来るかも
    category TEXT NOT NULL,
    -- 配当年次 「1年以上」みたいな感じで来る。intにするかD1みたいな区別を避けるためにTEXTにするか
    eligible_year TEXT NOT NULL,
    -- 単位数
    credits INT NOT NULL,
    -- 使用教室
    classroom TEXT NOT NULL,
    -- キャンパス
    campus TEXT NOT NULL,
    -- 科目キー
    course_key TEXT NOT NULL,
    -- 科目クラスコード
    class_code TEXT NOT NULL,
    -- 授業で使用する言語
    language TEXT NOT NULL,
    -- 授業形式 ENUMでいいかも。
    delivery_mode TEXT NOT NULL,
    -- コース・コード
    course_code TEXT NOT NULL,
    -- 大分野名称
    field_large TEXT,
    -- 中分野名称
    field_middle TEXT,
    -- 小分野名称
    field_small TEXT,
    -- レベル
    level TEXT,
    -- 授業形態
    class_format TEXT,

    -- 副題
    subtitle TEXT NOT NULL,
    -- 授業概要
    overview TEXT NOT NULL,
    -- 授業の到達目標
    objectives TEXT NOT NULL,
    -- 事前・事後学習の内容
    before_after_study TEXT NOT NULL,
    -- 授業計画
    lesson_plan TEXT NOT NULL,
    -- 教科書
    textbook TEXT NOT NULL,
    -- 参考文献
    reference_text TEXT NOT NULL,
    -- 成績評価方法
    granding_policy TEXT NOT NULL,
    -- 備考・関連URL
    remarks TEXT
    -- シラバス最終更新日
    syllabus_updated_at TEXT,

    source_url TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
)