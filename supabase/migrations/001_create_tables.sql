-- ============================================================
-- Museum Visitor Prediction — Supabase Schema
-- ============================================================

-- 1. Historical visitor data
CREATE TABLE IF NOT EXISTS visitor_data (
    id                      BIGSERIAL PRIMARY KEY,
    date                    DATE        NOT NULL UNIQUE,
    year                    SMALLINT    NOT NULL,
    month                   SMALLINT    NOT NULL,
    day                     SMALLINT    NOT NULL,
    day_of_week             SMALLINT    NOT NULL,
    day_name                TEXT        NOT NULL,
    week_of_year            SMALLINT    NOT NULL,
    quarter                 SMALLINT    NOT NULL,
    is_public_holiday       SMALLINT    NOT NULL DEFAULT 0,
    is_school_holiday       SMALLINT    NOT NULL DEFAULT 0,
    temperature             NUMERIC(5,2),
    precipitation           NUMERIC(6,2),
    weather_type            TEXT,
    special_exhibition      SMALLINT    NOT NULL DEFAULT 0,
    local_event             SMALLINT    NOT NULL DEFAULT 0,
    marketing_campaign      SMALLINT    NOT NULL DEFAULT 0,
    ticket_promotion        SMALLINT    NOT NULL DEFAULT 0,
    ticket_price            NUMERIC(6,2),
    visitors                INTEGER     NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_visitor_data_date ON visitor_data(date);

-- 2. Predictions log
CREATE TABLE IF NOT EXISTS predictions_log (
    id                      BIGSERIAL PRIMARY KEY,
    predicted_for_date      DATE        NOT NULL,
    predicted_visitors      INTEGER     NOT NULL,
    lower_80                INTEGER,
    upper_80                INTEGER,
    lower_95                INTEGER,
    upper_95                INTEGER,
    traffic_tier            TEXT,
    confidence              NUMERIC(5,4),
    model_used              TEXT,
    temperature             NUMERIC(5,2),
    precipitation           NUMERIC(6,2),
    weather_type            TEXT,
    special_exhibition      SMALLINT    DEFAULT 0,
    local_event             SMALLINT    DEFAULT 0,
    marketing_campaign      SMALLINT    DEFAULT 0,
    ticket_promotion        SMALLINT    DEFAULT 0,
    ticket_price            NUMERIC(6,2),
    actual_visitors         INTEGER,        -- filled in later when known
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_predictions_log_date ON predictions_log(predicted_for_date);
