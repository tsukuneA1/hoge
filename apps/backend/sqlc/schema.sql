CREATE TABLE syllabuses (
    id CHAR(28) PRIMARY KEY,
    title TEXT NOT NULL,
    title_en TEXT,
    year SMALLINT NOT NULL,
    semester VARCHAR(10) NOT NULL,
    credits SMALLINT,
    department TEXT,
    instructors TEXT[] NOT NULL DEFAULT '{}',

    description TEXT,
    objectives TEXT,
    schedule JSONB,
    evaluation TEXT,
    textbooks TEXT,
    crawled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);