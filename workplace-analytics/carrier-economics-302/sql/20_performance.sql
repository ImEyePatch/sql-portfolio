DROP VIEW IF EXISTS v_carrier_scorecard;
CREATE VIEW v_carrier_scorecard AS
SELECT carrier,COUNT(*) AS orders,SUM(revenue) AS revenue,
 SUM(total_carrier_cost) AS carrier_cost,
 SUM(gross_margin) AS gross_margin,
 ROUND(100.0*SUM(gross_margin)/NULLIF(SUM(revenue),0),2) AS weighted_margin_pct,
 SUM(CASE WHEN arrived_on_time=1 THEN 1 ELSE 0 END) AS on_time_orders,
 SUM(CASE WHEN arrived_on_time IS NOT NULL THEN 1 ELSE 0 END) AS scored_orders,
 ROUND(100.0*SUM(CASE WHEN arrived_on_time=1 THEN 1 ELSE 0 END)/
 NULLIF(SUM(CASE WHEN arrived_on_time IS NOT NULL THEN 1 ELSE 0 END),0),2) AS arrival_on_time_pct
FROM v_order_economics GROUP BY carrier;

DROP VIEW IF EXISTS v_lane_profitability;
CREATE VIEW v_lane_profitability AS
SELECT lane,COUNT(*) AS orders,SUM(revenue) AS revenue,
 SUM(total_carrier_cost) AS carrier_cost,SUM(gross_margin) AS gross_margin,
 ROUND(100.0*SUM(gross_margin)/NULLIF(SUM(revenue),0),2) AS weighted_margin_pct
FROM v_order_economics GROUP BY lane;

DROP VIEW IF EXISTS v_confirmation_timing;
CREATE VIEW v_confirmation_timing AS
SELECT carrier,COUNT(*) confirmations_with_order,
 AVG(confirmation_elapsed_hours) AS avg_confirmation_hours,
 SUM(CASE WHEN rate_confirmation_count>1 THEN 1 ELSE 0 END) AS multi_confirmation_orders
FROM v_order_economics WHERE rate_confirmation_count>0 GROUP BY carrier;
