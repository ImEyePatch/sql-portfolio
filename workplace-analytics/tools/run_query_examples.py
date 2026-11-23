"""Print a handful of synthetic KPI queries. Run from any directory."""
import sys
from demo_db import conn_for,PROJECTS

VIEWS={
 'usps-service-reconciliation':['v_case_match_audit','v_service_scenarios','v_lane_scoreboard','v_carrier_disagreements'],
 'carrier-noncompliance':['v_weekly_compliance','v_weekly_carrier_rates','v_week_over_week','v_lane_concentration'],
 'carrier-economics-302':['v_order_economics','v_carrier_scorecard','v_lane_profitability','v_confirmation_timing'],
 'trailer-tracking-addendum':['v_latest_event','v_asset_asof_order','v_asset_status'],
}
if len(sys.argv)!=2 or sys.argv[1] not in PROJECTS:
    print('Usage: python tools/run_query_examples.py <'+ '|'.join(PROJECTS)+'>');sys.exit(2)
with conn_for(sys.argv[1]) as db:
    for view in VIEWS[sys.argv[1]]:
        print('\n##',view)
        for row in db.execute(f'SELECT * FROM {view} LIMIT 4'):
            print(dict(row))
