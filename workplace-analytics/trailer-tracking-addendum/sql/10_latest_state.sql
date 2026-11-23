DROP VIEW IF EXISTS v_latest_event;
CREATE VIEW v_latest_event AS
SELECT * FROM (
 SELECT e.*,ROW_NUMBER() OVER(PARTITION BY asset_id ORDER BY event_at DESC,event_id DESC) rn
 FROM tracking_events e
) x WHERE rn=1;

DROP VIEW IF EXISTS v_asset_asof_order;
CREATE VIEW v_asset_asof_order AS
SELECT * FROM (
 SELECT e.asset_id,e.event_at,e.event_id,t.order_id,t.departed_at,t.expected_return_at,
 t.carrier,t.route,t.movement_status,
 ROW_NUMBER() OVER(PARTITION BY e.asset_id ORDER BY CASE WHEN t.departed_at IS NULL THEN 1 ELSE 0 END,
 t.departed_at DESC,t.order_id DESC) rn
 FROM v_latest_event e LEFT JOIN trip_orders t ON t.asset_id=e.asset_id
 AND t.departed_at<=e.event_at
) x WHERE rn=1;

DROP VIEW IF EXISTS v_asset_status;
CREATE VIEW v_asset_status AS
SELECT e.asset_id,e.event_at,e.city,e.region,e.motion_status,e.speed_mph,e.idle_hours,
 o.order_id,o.carrier,o.route,o.expected_return_at,
 CASE WHEN o.order_id IS NULL THEN 'out_of_network'
      WHEN h.city IS NOT NULL THEN 'approved_hub'
      WHEN e.idle_hours>48 THEN 'abandon_review'
      WHEN o.expected_return_at IS NOT NULL AND e.event_at>o.expected_return_at THEN 'delayed'
      ELSE 'ok' END AS business_status
FROM v_latest_event e LEFT JOIN v_asset_asof_order o ON o.asset_id=e.asset_id
LEFT JOIN approved_hubs h ON h.city=e.city AND h.region=e.region;
