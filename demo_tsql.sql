WITH RentalsEnriched AS (
    SELECT
        r.rental_id,
        r.start_time,
        r.end_time,
        DATEDIFF(MINUTE, r.start_time, r.end_time) AS duration_min,
        r.user_type,
        s.plan_type
    FROM dbo.BixiRentals AS r
    LEFT JOIN dbo.BixiSubscriptions AS s
        ON r.subscription_id = s.subscription_id
)
SELECT
    YEAR(start_time) AS rental_year,
    MONTH(start_time) AS rental_month,
    user_type,
    plan_type,
    COUNT(*) AS total_rides,
    AVG(duration_min) AS avg_duration_min,
    SUM(CASE WHEN duration_min <= 5 THEN 1 ELSE 0 END) AS short_rides,
    SUM(CASE WHEN duration_min BETWEEN 6 AND 30 THEN 1 ELSE 0 END) AS medium_rides,
    SUM(CASE WHEN duration_min > 30 THEN 1 ELSE 0 END) AS long_rides
FROM RentalsEnriched
GROUP BY
    YEAR(start_time),
    MONTH(start_time),
    user_type,
    plan_type
ORDER BY
    rental_year,
    rental_month,
    user_type,
    plan_type;