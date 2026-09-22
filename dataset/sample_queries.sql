-- Replace YOUR_PROJECT with your GCP project ID.

-- 1. Top 10 most populated cities in the world
SELECT city, country, total_population
FROM `YOUR_PROJECT.world_population.cities`
ORDER BY total_population DESC LIMIT 10;

-- 2. Male vs female population by continent
SELECT continent, male_population, female_population, ROUND(male_pct*100,1) AS male_pct
FROM `YOUR_PROJECT.world_population.continents`
ORDER BY total_population DESC;

-- 3. States in India ranked by population in listed cities
SELECT state_province, subdivision_type, cities_listed_15k, population_in_listed_cities, largest_city
FROM `YOUR_PROJECT.world_population.states_provinces`
WHERE country = 'India'
ORDER BY population_in_listed_cities DESC;

-- 4. Countries where deaths exceed births (shrinking naturally)
SELECT country, avg_births_per_year, avg_deaths_per_year, natural_growth_per_year
FROM `YOUR_PROJECT.world_population.countries`
WHERE natural_growth_per_year < 0
ORDER BY natural_growth_per_year;

-- 5. Full hierarchy for one country (join cities to country totals)
SELECT c.continent, c.country, c.state_province, c.subdivision_type, c.city,
       c.total_population, k.total_population AS country_population,
       ROUND(c.total_population / k.total_population * 100, 2) AS pct_of_country
FROM `YOUR_PROJECT.world_population.cities` c
JOIN `YOUR_PROJECT.world_population.countries` k USING (country)
WHERE c.country = 'United States'
ORDER BY c.total_population DESC;

-- 6. Most densely populated countries (people per km² of land)
SELECT country, total_population, land_area_km2, pop_density_per_km2
FROM `YOUR_PROJECT.world_population.countries`
WHERE land_area_km2 > 0
ORDER BY pop_density_per_km2 DESC LIMIT 15;

-- 7. Continent size and density
SELECT continent, surface_area_km2, land_area_km2, pop_density_per_km2
FROM `YOUR_PROJECT.world_population.continents`
ORDER BY land_area_km2 DESC;

-- 8. Largest cities by recorded area (Wikidata city limits)
SELECT city, country, area_km2, total_population, pop_density_per_km2
FROM `YOUR_PROJECT.world_population.cities`
WHERE area_km2 IS NOT NULL
ORDER BY area_km2 DESC LIMIT 20;

-- 9. The 10 largest lakes, with the countries they touch
SELECT name, feature_type, area_km2, countries
FROM `YOUR_PROJECT.world_population.geo_features`
WHERE category = 'Lake'
ORDER BY area_km2 DESC LIMIT 10;

-- 10. Seas and islands bordering one country
SELECT category, feature_type, name, area_km2
FROM `YOUR_PROJECT.world_population.geo_features`
WHERE countries LIKE '%India%'
ORDER BY category, area_km2 DESC;
