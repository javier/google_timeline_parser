SELECT
  MIN(previous_date) AS date_from,
  MAX(date) AS date_to,
  GREATEST(0, DATEDIFF(CAST(MAX(date) AS timestamp),CAST(MIN(previous_date) AS timestamp)) -1) AS days,
  CONCAT('UK>', GROUP_CONCAT(country, '>')) AS itinerary,
  trip_no
FROM (
  SELECT
    *,
    SUM(IF(previous_country='UK',1,0)) OVER (ORDER BY timestamp ASC) AS trip_no
  FROM (
    SELECT
      *,
      REGEXP_EXTRACT(previous_locality, r'(\w+$)') AS previous_country,
      REGEXP_EXTRACT(locality, r'(\w+$)') AS country,
    FROM (
      SELECT
        timestamp,
        LAG(date, 1) OVER (ORDER BY timestamp ASC) AS previous_date,
        LAG(locality, 1) OVER (ORDER BY timestamp ASC) AS previous_locality,
        date,
        locality
      FROM
        [javier-cp300:locations.history]
      WHERE
        locality <> 'Error' ) )
  WHERE
    previous_country <> country )
GROUP BY
  trip_no
ORDER BY
  trip_no
