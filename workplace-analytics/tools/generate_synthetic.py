"""Generate explicitly fictional datasets for the public case studies."""
from demo_db import conn_for, export_csv, EXPORT_VIEWS, ROOT
from pathlib import Path

NAMES={
 'usps-service-reconciliation':'scored_events.csv',
 'carrier-noncompliance':'weekly_compliance.csv',
 'carrier-economics-302':'order_economics.csv',
 'trailer-tracking-addendum':'asset_status.csv',
}
for project,view in EXPORT_VIEWS.items():
    with conn_for(project) as con:
        export_csv(con,view,ROOT/project/'data'/NAMES[project])
        print(f'{project}: {NAMES[project]} created from synthetic rows')
