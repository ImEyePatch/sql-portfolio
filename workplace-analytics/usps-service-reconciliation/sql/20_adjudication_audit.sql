-- An adjudication applies ONLY to one uniquely matched load/event-type/scheduled-time.
DROP VIEW IF EXISTS v_case_match_audit;
CREATE VIEW v_case_match_audit AS
SELECT a.case_id,a.decision,a.load_id,a.event_type,a.scheduled_at,
       COUNT(e.event_id) AS matched_event_count,
       CASE WHEN a.event_type IS NULL OR a.scheduled_at IS NULL THEN 'insufficient_event_key'
            WHEN COUNT(e.event_id)=0 THEN 'unmatched'
            WHEN COUNT(e.event_id)>1 THEN 'ambiguous'
            WHEN a.decision='approved' THEN 'approved_unique'
            WHEN a.decision='pending' THEN 'pending_unique'
            ELSE 'denied_unique' END AS match_status,
       CASE WHEN COUNT(e.event_id)=1 THEN MAX(e.event_id) END AS matched_event_id
FROM adjudications a LEFT JOIN usps_events e
 ON e.load_id=a.load_id AND e.event_type=a.event_type
 AND e.scheduled_at=a.scheduled_at
GROUP BY a.case_id,a.decision,a.load_id,a.event_type,a.scheduled_at;

DROP VIEW IF EXISTS v_scored_events;
CREATE VIEW v_scored_events AS
WITH audit AS (
 SELECT matched_event_id AS event_id,
 MAX(CASE WHEN match_status='approved_unique' THEN 1 ELSE 0 END) approved,
 MAX(CASE WHEN match_status='pending_unique' THEN 1 ELSE 0 END) pending
 FROM v_case_match_audit WHERE matched_event_id IS NOT NULL GROUP BY matched_event_id
)
SELECT r.*,
 CASE WHEN r.usps_on_time IS NOT NULL AND COALESCE(a.approved,0)=1 THEN 1 ELSE 0 END AS approved_exclusion,
 CASE WHEN r.usps_on_time IS NOT NULL AND COALESCE(a.pending,0)=1 THEN 1 ELSE 0 END AS pending_exclusion,
 CASE WHEN r.usps_on_time IS NOT NULL THEN 1 ELSE 0 END AS scored_before,
 CASE WHEN r.usps_on_time IS NOT NULL AND COALESCE(a.approved,0)=0 THEN 1 ELSE 0 END AS scored_after,
 CASE WHEN r.usps_on_time IS NOT NULL AND COALESCE(a.approved,0)=0 AND COALESCE(a.pending,0)=0 THEN 1 ELSE 0 END AS scored_if_pending_approved
FROM v_event_reconciliation r LEFT JOIN audit a ON a.event_id=r.event_id;
