-- ============================================================
-- Seed: load CSV into visitor_data table
-- Run this in the Supabase SQL editor after creating the table
-- and uploading the CSV via Storage or psql COPY.
-- ============================================================

-- Option A: if you have direct psql access (Railway / local Postgres)
-- \copy visitor_data (date,year,month,day,day_of_week,day_name,week_of_year,
--   quarter,is_public_holiday,is_school_holiday,temperature,precipitation,
--   weather_type,special_exhibition,local_event,marketing_campaign,
--   ticket_promotion,ticket_price,visitors_last_week,visitors_last_2weeks,
--   visitors_last_month,visitors_7day_avg,visitors_14day_avg,visitors_30day_avg,
--   visitors_same_day_last_year,visitors)
-- FROM '/absolute/path/to/data/raw/museum_visitors_melbourne.csv'
-- CSV HEADER;

-- Option B: Supabase SQL editor — paste this after uploading via Table Editor
-- (Supabase UI > Table Editor > Import CSV is the easiest route)

-- Verify row count after import:
SELECT COUNT(*) AS total_rows FROM visitor_data;
SELECT MIN(date) AS earliest, MAX(date) AS latest FROM visitor_data;
