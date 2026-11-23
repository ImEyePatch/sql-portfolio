DROP VIEW IF EXISTS v_weekly_carrier_rates;
CREATE VIEW v_weekly_carrier_rates AS
SELECT week_start,carrier,COUNT(*) AS flagged_loads,
 SUM(CASE WHEN excluded_no_movement=0 THEN 1 ELSE 0 END) AS eligible_loads,
 SUM(CASE WHEN failure_category NOT IN ('compliant','excluded_no_movement') THEN 1 ELSE 0 END) AS noncompliant_loads,
 SUM(geofence_failure) AS geofence_failed,
 SUM(ping_failure) AS ping_failed,
 SUM(excluded_no_movement) AS excluded_loads,
 ROUND(100.0*SUM(CASE WHEN failure_category NOT IN ('compliant','excluded_no_movement') THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN excluded_no_movement=0 THEN 1 ELSE 0 END),0),2) AS noncompliance_pct
FROM v_weekly_compliance GROUP BY week_start,carrier;

DROP VIEW IF EXISTS v_week_over_week;
CREATE VIEW v_week_over_week AS
SELECT w.*,p.noncompliant_loads AS prior_week_noncompliant,
 CASE WHEN p.noncompliant_loads IS NULL OR p.noncompliant_loads=0 THEN NULL
 ELSE ROUND(100.0*(w.noncompliant_loads-p.noncompliant_loads)/p.noncompliant_loads,2) END AS wow_noncompliance_change_pct
FROM v_weekly_carrier_rates w LEFT JOIN v_weekly_carrier_rates p
 ON p.carrier=w.carrier AND p.week_start=date(w.week_start,'-7 days');

DROP VIEW IF EXISTS v_lane_concentration;
CREATE VIEW v_lane_concentration AS
SELECT week_start,lane,COUNT(*) AS loads,
 SUM(CASE WHEN failure_category NOT IN ('compliant','excluded_no_movement') THEN 1 ELSE 0 END) AS noncompliant_loads,
 ROUND(100.0*SUM(CASE WHEN failure_category NOT IN ('compliant','excluded_no_movement') THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN excluded_no_movement=0 THEN 1 ELSE 0 END),0),2) AS failure_pct
FROM v_weekly_compliance GROUP BY week_start,lane;
