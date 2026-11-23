-- Aggregate the 1:N driver-pay detail BEFORE joining orders, or costs are multiplied.
DROP VIEW IF EXISTS v_order_economics;
CREATE VIEW v_order_economics AS
WITH driver_agg AS (
 SELECT order_id,SUM(amount) AS extra_pay,COUNT(*) AS extra_pay_lines
 FROM driver_extra_pay GROUP BY order_id
), rc AS (
 SELECT r.order_id,MIN(r.issued_at) AS first_issued_at,
 -- MAX acknowledged timestamp deliberately models latest acknowledge, not the first.
 MAX(r.acknowledged_at) AS latest_acknowledged_at,
 COUNT(*) AS rate_confirmation_count
 FROM rate_confirmations r GROUP BY order_id
)
SELECT o.order_id,o.carrier,o.lane,o.trip_id,
 o.revenue,o.base_carrier_cost,COALESCE(d.extra_pay,0) AS extra_pay,
 o.base_carrier_cost+COALESCE(d.extra_pay,0) AS total_carrier_cost,
 o.revenue-o.base_carrier_cost-COALESCE(d.extra_pay,0) AS gross_margin,
 ROUND(100.0*(o.revenue-o.base_carrier_cost-COALESCE(d.extra_pay,0))/NULLIF(o.revenue,0),2) AS gross_margin_pct,
 o.scheduled_arrival,o.actual_arrival,
 CASE WHEN o.actual_arrival IS NULL OR o.scheduled_arrival IS NULL THEN NULL
 WHEN (julianday(o.actual_arrival)-julianday(o.scheduled_arrival))*1440<=15.001 THEN 1 ELSE 0 END AS arrived_on_time,
 t.miles,t.planned_drive_hours,t.actual_drive_hours,
 r.first_issued_at,r.latest_acknowledged_at,r.rate_confirmation_count,
 CASE WHEN r.latest_acknowledged_at IS NULL THEN NULL
 ELSE ROUND((julianday(r.latest_acknowledged_at)-julianday(r.first_issued_at))*24,2) END AS confirmation_elapsed_hours
FROM orders o
LEFT JOIN driver_agg d ON d.order_id=o.order_id
LEFT JOIN trips t ON t.trip_id=o.trip_id
LEFT JOIN rc r ON r.order_id=o.order_id;
