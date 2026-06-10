CREATE TYPE CRAWL_JOB_TYPE AS ENUM (
    'discover',
    'ingest'
);

CREATE TYPE CRAWL_RUN_STATUS AS ENUM (
    'running',
    'succeeded',
    'partially_succeeded',
    'failed'
);

CREATE TYPE CRAWL_TARGET_STATUS AS ENUM (
    'pending',
    'running',
    'succeeded',
    'failed'
);

CREATE TABLE crawl_runs (
    id BIGSERIAL PRIMARY KEY,

    job_type CRAWL_JOB_TYPE NOT NULL,
    status CRAWL_RUN_STATUS NOT NULL,

    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at TIMESTAMPTZ,

    discovered_count INTEGER NOT NULL DEFAULT 0,
    ingested_count INTEGER NOT NULL DEFAULT 0,
    failed_count INTEGER NOT NULL DEFAULT 0,

    error_message TEXT
);

CREATE TABLE crawl_targets (
    pkey TEXT PRIMARY KEY,

    last_seen_run_id BIGINT REFERENCES crawl_runs (id),

    status CRAWL_TARGET_STATUS NOT NULL DEFAULT 'pending',
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

-- 現時点で明確に検索条件に含まれるものだけインデックスを作成
CREATE INDEX idx_crawl_targets_status ON crawl_targets (status);

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
    category TEXT,
    -- 配当年次 「1年以上」みたいな感じで来る。intにするかD1みたいな区別を避けるためにTEXTにするか
    eligible_year TEXT,
    -- 単位数
    -- これが取れないことは流石にないはず。整数を正規表現でとればよいだけ
    credits INT NOT NULL,
    -- 使用教室
    classroom TEXT,
    -- キャンパス
    campus TEXT,
    -- 科目キー
    course_key TEXT,
    -- 科目クラスコード
    class_code TEXT,
    -- 授業で使用する言語
    language TEXT,
    -- 授業形式 ENUMでいいかも。
    delivery_mode TEXT,
    -- コース・コード
    course_code TEXT,
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
    subtitle TEXT,
    -- 授業概要
    overview TEXT,
    -- 授業の到達目標
    objectives TEXT,
    -- 事前・事後学習の内容
    before_after_study TEXT,
    -- 授業計画
    lesson_plan TEXT,
    -- 教科書
    textbook TEXT,
    -- 参考文献
    reference_text TEXT,
    -- 成績評価方法
    grading_policy TEXT,
    -- 備考・関連URL
    remarks TEXT,
    -- シラバス最終更新日
    syllabus_updated_at TEXT,

    source_url TEXT NOT NULL,
    -- 一旦カラムだけ置く。データ量がボトルネックになるならNULLで入れる
    raw_html TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
