-- Rebuilt from high-level architecture; does not reproduce employer source code.
-- Grain: one USPS event. 15-minute threshold is an illustrative parameter.
DROP VIEW IF EXISTS v_event_reconciliation;
CREATE VIEW v_event_reconciliation AS
SELECT e.event_id,e.load_id,o.trip_id,o.carrier,e.lane,e.event_type,
  e.scheduled_at,e.actual_at,
  CASE WHEN e.actual_at IS NULL THEN NULL
       ELSE ROUND((julianday(e.actual_at)-julianday(e.scheduled_at))*1440,2) END AS usps_delta_minutes,
  CASE WHEN e.actual_at IS NULL THEN NULL
       WHEN (julianday(e.actual_at)-julianday(e.scheduled_at))*1440<=15.001 THEN 1 ELSE 0 END AS usps_on_time,
  CASE WHEN e.event_type='departure' THEN o.origin_sched_departure ELSE o.destination_sched_arrival END AS tms_scheduled_at,
  CASE WHEN e.event_type='departure' THEN o.origin_actual_departure ELSE o.destination_actual_arrival END AS tms_actual_at,
  CASE WHEN (CASE WHEN e.event_type='departure' THEN o.origin_actual_departure ELSE o.destination_actual_arrival END) IS NULL THEN NULL
       WHEN (julianday(CASE WHEN e.event_type='departure' THEN o.origin_actual_departure ELSE o.destination_actual_arrival END)-
             julianday(CASE WHEN e.event_type='departure' THEN o.origin_sched_departure ELSE o.destination_sched_arrival END))*1440<=15.001
       THEN 1 ELSE 0 END AS tms_on_time,
  CASE WHEN e.actual_at IS NOT NULL AND
        (CASE WHEN e.event_type='departure' THEN o.origin_actual_departure ELSE o.destination_actual_arrival END) IS NOT NULL
       THEN 1 ELSE 0 END AS eligible_for_comparison
FROM usps_events e JOIN orders o ON o.load_id=e.load_id;
