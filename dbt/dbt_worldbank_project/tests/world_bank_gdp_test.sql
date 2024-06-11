-- This SQL file defines test case for the world_bank_gdp  model

-- Test: Check for missing data in required columns
-- configured to fail if the output is != 0
SELECT count(*)
FROM {{ ref('world_bank_gdp')}}
WHERE "Country" IS NULL OR "Year" IS NULL OR "Gdp" IS NULL

