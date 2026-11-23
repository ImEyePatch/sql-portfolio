"""Self-contained SQLite demonstration runner; source rows are invented fixtures.

No production database, network call, credential or third-party package is needed.
"""
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parent.parent
PROJECTS={
 'usps-service-reconciliation':['orders','usps_events','adjudications','lane_benchmarks'],
 'carrier-noncompliance':['loads','weekly_snapshots','geofence_events'],
 'carrier-economics-302':['orders','trips','driver_extra_pay','rate_confirmations'],
 'trailer-tracking-addendum':['assets','tracking_events','trip_orders','approved_hubs'],
}

def conn_for(project):
    if project not in PROJECTS:raise ValueError('Unknown project')
    con=sqlite3.connect(':memory:')
    con.row_factory=sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript((ROOT/project/'sql/00_schema.sql').read_text())
    seed(con,project)
    for sql in sorted((ROOT/project/'sql').glob('[1-9]*.sql')):
        con.executescript(sql.read_text())
    return con

def insert(con,table,columns,rows):
    q=f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})"
    con.executemany(q,rows)

def seed(con,project):
    if project=='usps-service-reconciliation':
        rows=[
        ('DEMO-01','T-A','ALPHA-BETA','Carrier North','2026-01-05 08:00','2026-01-05 08:04','2026-01-05 11:00','2026-01-05 11:24'),
        ('DEMO-02','T-B','ALPHA-BETA','Carrier South','2026-01-05 08:00','2026-01-05 08:30','2026-01-05 11:00','2026-01-05 11:07'),
        ('DEMO-03','T-C','BETA-GAMMA','Carrier North','2026-01-06 08:00','2026-01-06 08:40','2026-01-06 11:00','2026-01-06 11:50'),
        ('DEMO-04','T-D','BETA-GAMMA','Carrier East','2026-01-07 08:00','2026-01-07 07:58','2026-01-07 11:00','2026-01-07 10:58'),
        ('DEMO-05','T-E','ALPHA-BETA','Carrier East','2026-01-08 08:00',None,'2026-01-08 11:00','2026-01-08 11:10'),
        ('DEMO-06','T-F','GAMMA-DELTA','Carrier South','2026-01-09 08:00','2026-01-09 08:20','2026-01-09 11:00','2026-01-09 11:30'),
        ]
        insert(con,'orders',['load_id','trip_id','lane','carrier','origin_sched_departure','origin_actual_departure','destination_sched_arrival','destination_actual_arrival'],rows)
        events=[]
        for i,row in enumerate(rows,1):
            load,_,lane,_,dep_s,dep_a,arr_s,arr_a=row
            # For a single event, make the USPS verdict disagree with the TMS.
            usps_dep_a=('2026-01-05 08:05' if i==2 else ('2026-01-07 08:30' if i==4 else dep_a))
            events.extend([(f'EV-{i:02d}-D',load,'departure',dep_s,usps_dep_a,lane),
                           (f'EV-{i:02d}-A',load,'arrival',arr_s,arr_a,lane)])
        insert(con,'usps_events',['event_id','load_id','event_type','scheduled_at','actual_at','lane'],events)
        cases=[('C01','DEMO-02','departure','2026-01-05 08:00','approved'),
        ('C02','DEMO-06','arrival','2026-01-09 11:00','approved'),
        ('C03','DEMO-03','departure','2026-01-06 08:00','pending'),
        ('C04','DEMO-03','arrival','2026-01-06 11:00','pending'),
        ('C05','UNKNOWN','departure','2026-01-01 08:00','approved'),
        ('C06','DEMO-05',None,None,'approved'),
        ('C07','DEMO-01','arrival','2026-01-05 11:00','denied')]
        insert(con,'adjudications',['case_id','load_id','event_type','scheduled_at','decision'],cases)
        insert(con,'lane_benchmarks',['lane','reported_departure_rate','reported_arrival_rate','reported_departure_events','reported_arrival_events'],[
           ('ALPHA-BETA',82.,78.,18,18),('BETA-GAMMA',70.,80.,12,12),('GAMMA-DELTA',62.,61.,8,8)])
    elif project=='carrier-noncompliance':
        loads=[('LOAD-A','Carrier North','A-B','2026-01-05',2),('LOAD-B','Carrier North','A-B','2026-01-05',3),
               ('LOAD-C','Carrier South','B-C',None,2),('LOAD-D','Carrier East','C-D','2026-01-05',2),
               ('LOAD-E','Carrier South','B-C','2026-01-12',3),('LOAD-F','Carrier East','C-D','2026-01-12',2)]
        insert(con,'loads',['load_id','carrier','lane','departed_at','expected_stops'],loads)
        snap=[('S01','LOAD-A','2026-01-05',10,2,2,1),('S02','LOAD-B','2026-01-05',50,1,3,1),
              ('S03','LOAD-C','2026-01-05',10,0,2,0),('S04','LOAD-D','2026-01-05',50,2,2,1),
              ('S05','LOAD-A','2026-01-12',5,2,2,1),('S06','LOAD-B','2026-01-12',10,1,3,1),
              ('S07','LOAD-E','2026-01-12',10,3,3,1),('S08','LOAD-F','2026-01-12',None,2,2,1),
              ('S09','LOAD-B','2026-01-12',45,1,3,1)]
        insert(con,'weekly_snapshots',['snapshot_id','load_id','week_start','ping_interval_min','geofence_stops_detected','geofence_stops_expected','has_movement'],snap)
        insert(con,'geofence_events',['id','load_id','facility','event_type','event_at','appointment_at'],[
          ('G1','LOAD-A','HUB-1','arrival','2026-01-05 10:00','2026-01-05 10:00'),
          ('G2','LOAD-B','HUB-2','arrival',None,'2026-01-06 10:00')])
    elif project=='carrier-economics-302':
        orders=[('O-A','Carrier North','A-B','2026-01-05 10:00','2026-01-05 10:12',1000.,700.,'T1'),
        ('O-B','Carrier South','A-B','2026-01-05 12:00','2026-01-05 12:30',1200.,850.,'T2'),
        ('O-C','Carrier North','B-C','2026-01-06 14:00',None,900.,650.,'T3'),
        ('O-D','Carrier East','C-D','2026-01-07 09:00','2026-01-07 08:59',1400.,1000.,'T4')]
        insert(con,'orders',['order_id','carrier','lane','scheduled_arrival','actual_arrival','revenue','base_carrier_cost','trip_id'],orders)
        insert(con,'trips',['trip_id','trip_lane','miles','planned_drive_hours','actual_drive_hours'],[
          ('T1','A-B',100,2.5,2.6),('T2','A-B',100,2.5,3.1),('T3','B-C',150,3.,None),('T4','C-D',175,4.,3.9)])
        insert(con,'driver_extra_pay',['pay_id','order_id','pay_code','amount'],[
          ('P1','O-A','EXTRA',35.),('P2','O-A','WAIT',20.),('P3','O-B','FUEL',10.)])
        insert(con,'rate_confirmations',['confirmation_id','order_id','issued_at','acknowledged_at'],[
          ('RC1','O-A','2026-01-04 08:00','2026-01-04 09:30'),
          ('RC2','O-B','2026-01-04 08:00','2026-01-04 10:00'),
          ('RC3','O-B','2026-01-04 10:30','2026-01-04 11:00')])
    elif project=='trailer-tracking-addendum':
        insert(con,'assets',['asset_id','provider'],[('ASSET-A','Provider A'),('ASSET-B','Provider B'),('ASSET-C','Provider A'),('ASSET-D','Provider B')])
        insert(con,'tracking_events',['event_id','asset_id','event_at','city','region','motion_status','speed_mph','idle_hours'],[
          ('E1','ASSET-A','2026-01-06 08:00','City A','AA','moving',45.,0.),
          ('E2','ASSET-A','2026-01-06 13:00','City B','BB','stopped',0.,52.),
          ('E3','ASSET-B','2026-01-06 09:00','City C','CC','stopped',0.,70.),
          ('E4','ASSET-C','2026-01-06 10:00','City D','DD','moving',30.,0.),
          ('E5','ASSET-D','2026-01-07 13:00','City E','EE','moving',25.,0.)])
        insert(con,'approved_hubs',['city','region'],[('City C','CC')])
        insert(con,'trip_orders',['order_id','asset_id','departed_at','arrived_at','expected_return_at','carrier','route','movement_status'],[
          ('ORD-1','ASSET-A','2026-01-05 09:00',None,'2026-01-10 08:00','Demo Carrier','A-B','active'),
          ('ORD-2','ASSET-B','2026-01-05 09:00',None,'2026-01-05 08:00','Demo Carrier','C-D','active'),
          ('ORD-3','ASSET-D','2026-01-04 09:00',None,'2026-01-06 08:00','Demo Carrier','D-E','active'),
          ('ORD-4','ASSET-A','2026-01-07 13:00',None,'2026-01-08 08:00','Demo Carrier','A-C','planned')])
    con.commit()

EXPORT_VIEWS={
 'usps-service-reconciliation':'v_scored_events',
 'carrier-noncompliance':'v_weekly_compliance',
 'carrier-economics-302':'v_order_economics',
 'trailer-tracking-addendum':'v_asset_status',
}

def export_csv(con,view,path):
    import csv
    query=con.execute(f'SELECT * FROM {view}')
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow([x[0] for x in query.description]);writer.writerows(query.fetchall())

if __name__=='__main__':
    import json
    for project,view in EXPORT_VIEWS.items():
        with conn_for(project) as con:
            path=ROOT/project/'data'/({'usps-service-reconciliation':'scored_events.csv','carrier-noncompliance':'weekly_compliance.csv','carrier-economics-302':'order_economics.csv','trailer-tracking-addendum':'asset_status.csv'}[project])
            export_csv(con,view,path)
            print(project,'exported',path.name,'rows',con.execute(f'SELECT COUNT(*) FROM {view}').fetchone()[0])
