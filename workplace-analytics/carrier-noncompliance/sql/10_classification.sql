DROP VIEW IF EXISTS v_latest_weekly_snapshot;
CREATE VIEW v_latest_weekly_snapshot AS
SELECT s.* FROM weekly_snapshots s JOIN (
 SELECT load_id,week_start,MAX(snapshot_id) AS last_snapshot
 FROM weekly_snapshots GROUP BY load_id,week_start
) x ON x.last_snapshot=s.snapshot_id;

DROP VIEW IF EXISTS v_weekly_compliance;
CREATE VIEW v_weekly_compliance AS
SELECT s.snapshot_id,s.week_start,s.load_id,l.carrier,l.lane,
  s.ping_interval_min,s.geofence_stops_expected,s.geofence_stops_detected,
  CASE WHEN s.has_movement=0 THEN 1 ELSE 0 END AS excluded_no_movement,
  CASE WHEN s.has_movement=1 AND COALESCE(s.geofence_stops_detected,-1)<s.geofence_stops_expected THEN 1 ELSE 0 END AS geofence_failure,
  -- 30 minutes is a synthetic demonstration threshold, NOT an employer policy
  CASE WHEN s.has_movement=1 AND (s.ping_interval_min IS NULL OR s.ping_interval_min>30) THEN 1 ELSE 0 END AS ping_failure,
  CASE WHEN s.has_movement=0 THEN 'excluded_no_movement'
       WHEN COALESCE(s.geofence_stops_detected,-1)<s.geofence_stops_expected AND (s.ping_interval_min IS NULL OR s.ping_interval_min>30) THEN 'both'
       WHEN COALESCE(s.geofence_stops_detected,-1)<s.geofence_stops_expected THEN 'geofence'
       WHEN s.ping_interval_min IS NULL OR s.ping_interval_min>30 THEN 'ping_frequency'
       ELSE 'compliant' END AS failure_category
FROM v_latest_weekly_snapshot s JOIN loads l ON l.load_id=s.load_id;
