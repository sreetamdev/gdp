
{{ config(materialized='table') }}

/*This section defines a CTE named source_data. 
The CTE selects data from the world_bank table and renames columns for better readability:
country is renamed to Country
Year is extracted from the date column using to_date and extract functions (assuming the date format is YYYY) and named Year
value is renamed to Gdp */
with source_data as (

	select "country" as "Country",
       		extract (YEAR from (to_date("date",'YYYY'))) as "Year",
       		"value" as "Gdp"
			from world_bank
	)


 /*This CTE builds upon source_data by adding a new column named rank.
The dense_rank function assigns a rank to each row within each country, ordered by Year. */   

,source_data_with_rank as (
  select s.*,
         dense_rank() over (partition by "Country" order by "Year") as "rank"
  from source_data s
)

/*This CTE calculates the GDP growth for each country and year. It uses a window function called 
lag to access the GDP value from the previous year within the same country partition. 
The calculation is:*/

,source_data_transformation_gdp_growth as (

	select 	sr.*,
			case when lag("Gdp") over (partition by "Country" order by "Year") is null then 0
       		else ("Gdp" - lag("Gdp") over (partition by "Country" order by "Year")) / lag("Gdp") over (partition by "Country" order by "Year")
  			end as "gdp_growth"
			from source_data_with_rank sr
			
)

/*This CTE calculates the minimum and maximum GDP growth for each country since the year 2000 to the current year the row represents (not to the latest year). 
It uses window functions again:

min function finds the minimum gdp_growth between the current row and all preceding rows within the same 
country partition, starting from the year 2000 (using ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW). 
This gives the minimum GDP growth since 2000 (up to the current year).

Similar logic applies to the max function to find the maximum GDP growth since 2000.
Additionally, it filters the data to include only rows where Gdp is not null and 
Year is greater than or equal to 2000.*/

,source_data_transformation_gdp_growth_min_max as
	
(
			select stg.*,
			min("gdp_growth") over (partition by "Country" order by "Year" ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as "min_gdp_growth_since_2000",
			max("gdp_growth") over (partition by "Country" order by "Year" ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as "max_gdp_growth_since_2000"
			from source_data_transformation_gdp_growth stg
			where "Gdp" is not null  
  			and "Year" >= 2000
)

/*The final select statement retrieves data from the last CTE (source_data_transformation_gdp_growth_min_max). 
It casts some columns to specific data types for better representation:*/

select 
"Country",
"Year",
CAST("Gdp" AS DECIMAL(32,2)) AS "Gdp",
CAST("gdp_growth" AS DECIMAL(10,4)) AS "gdp_growth",
CAST("min_gdp_growth_since_2000" AS DECIMAL(10,4)) AS "min_gdp_growth_since_2000",
CAST("max_gdp_growth_since_2000" AS DECIMAL(10,4)) AS "max_gdp_growth_since_2000"
	


	
from source_data_transformation_gdp_growth_min_max
