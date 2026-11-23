-- Denominator-changing exclusions; this is a SYNTHETIC illustration only.
DROP VIEW IF EXISTS v_service_scenarios;
CREATE VIEW v_service_scenarios AS
SELECT 'before' AS scenario, SUM(scored_before) scored_events,
 SUM(CASE WHEN scored_before=1 THEN usps_on_time ELSE 0 END) on_time_events,
 ROUND(100.0*SUM(CASE WHEN scored_before=1 THEN usps_on_time ELSE 0 END)/NULLIF(SUM(scored_before),0),2) on_time_pct
FROM v_scored_events
UNION ALL SELECT 'approved_excluded',SUM(scored_after),
 SUM(CASE WHEN scored_after=1 THEN usps_on_time ELSE 0 END),
 ROUND(100.0*SUM(CASE WHEN scored_after=1 THEN usps_on_time ELSE 0 END)/NULLIF(SUM(scored_after),0),2)
FROM v_scored_events
UNION ALL SELECT 'pending_approved_simulation',SUM(scored_if_pending_approved),
 SUM(CASE WHEN scored_if_pending_approved=1 THEN usps_on_time ELSE 0 END),
 ROUND(100.0*SUM(CASE WHEN scored_if_pending_approved=1 THEN usps_on_time ELSE 0 END)/NULLIF(SUM(scored_if_pending_approved),0),2)
FROM v_scored_events;

DROP VIEW IF EXISTS v_lane_scoreboard;
CREATE VIEW v_lane_scoreboard AS
SELECT e.lane,e.event_type,
 COUNT(*) AS matched_events,
 SUM(e.scored_before) AS scored_before,
 SUM(e.scored_after) AS scored_after,
 SUM(e.approved_exclusion) AS approved_excluded,
 ROUND(100.0*SUM(CASE WHEN e.scored_before=1 THEN e.usps_on_time ELSE 0 END)/NULLIF(SUM(e.scored_before),0),2) AS usps_pct_before,
 ROUND(100.0*SUM(CASE WHEN e.scored_after=1 THEN e.tms_on_time ELSE 0 END)/NULLIF(SUM(CASE WHEN e.scored_after=1 AND e.tms_on_time IS NOT NULL THEN 1 ELSE 0 END),0),2) AS tms_pct_after,
 CASE WHEN e.event_type='departure' THEN MAX(b.reported_departure_rate) ELSE MAX(b.reported_arrival_rate) END AS reported_pct
FROM v_scored_events e LEFT JOIN lane_benchmarks b ON b.lane=e.lane
GROUP BY e.lane,e.event_type;

DROP VIEW IF EXISTS v_carrier_disagreements;
CREATE VIEW v_carrier_disagreements AS
SELECT carrier,event_type,COUNT(*) AS comparable_events,
 SUM(CASE WHEN usps_on_time<>tms_on_time THEN 1 ELSE 0 END) AS disagreement_count,
 SUM(CASE WHEN usps_on_time=0 AND tms_on_time=1 THEN 1 ELSE 0 END) AS usps_late_tms_on_time,
 SUM(CASE WHEN usps_on_time=1 AND tms_on_time=0 THEN 1 ELSE 0 END) AS usps_on_time_tms_late
FROM v_scored_events
WHERE eligible_for_comparison=1 AND scored_after=1
GROUP BY carrier,event_type;
