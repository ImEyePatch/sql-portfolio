import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'python'))
from demo_db import conn_for

class TestUSPS(unittest.TestCase):
    def setUp(self):self.db=conn_for('usps-service-reconciliation')
    def tearDown(self):self.db.close()
    def test_event_grain_and_missing_time(self):
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM v_event_reconciliation').fetchone()[0],12)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM v_scored_events WHERE scored_before=0').fetchone()[0],1)
    def test_exact_event_adjudication(self):
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM v_case_match_audit WHERE match_status='approved_unique'").fetchone()[0],2)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM v_case_match_audit WHERE match_status='pending_unique'").fetchone()[0],2)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM v_case_match_audit WHERE match_status='unmatched'").fetchone()[0],1)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM v_case_match_audit WHERE match_status='insufficient_event_key'").fetchone()[0],1)
        self.assertEqual(self.db.execute('SELECT SUM(approved_exclusion) FROM v_scored_events').fetchone()[0],2)
    def test_pending_scenario_kept_separate(self):
        k={x['scenario']:tuple(x[c] for c in ('scored_events','on_time_events')) for x in self.db.execute('SELECT * FROM v_service_scenarios')}
        self.assertEqual(k['before'],(11,5))
        self.assertEqual(k['approved_excluded'],(9,4))
        self.assertEqual(k['pending_approved_simulation'],(7,4))
    def test_no_zero_division(self):
        self.assertGreater(self.db.execute('SELECT COUNT(*) FROM v_lane_scoreboard').fetchone()[0],0)
        self.assertGreater(self.db.execute('SELECT SUM(disagreement_count) FROM v_carrier_disagreements').fetchone()[0],0)

class TestNonCompliance(unittest.TestCase):
    def setUp(self):self.db=conn_for('carrier-noncompliance')
    def tearDown(self):self.db.close()
    def test_one_load_one_week(self):
        rows=self.db.execute('SELECT week_start,load_id,COUNT(*) n FROM v_weekly_compliance GROUP BY 1,2 HAVING n>1').fetchall()
        self.assertEqual(len(rows),0)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM v_weekly_compliance').fetchone()[0],8)
    def test_both_failure_not_double_counted(self):
        row=self.db.execute("SELECT * FROM v_weekly_compliance WHERE load_id='LOAD-B' AND week_start='2026-01-05'").fetchone()
        self.assertEqual(row['failure_category'],'both')
        x=self.db.execute("SELECT * FROM v_weekly_carrier_rates WHERE week_start='2026-01-05' AND carrier='Carrier North'").fetchone()
        self.assertEqual((x['noncompliant_loads'],x['geofence_failed'],x['ping_failed']),(1,1,1))
    def test_exclusion_and_weekly_trend(self):
        row=self.db.execute("SELECT * FROM v_weekly_carrier_rates WHERE week_start='2026-01-05' AND carrier='Carrier South'").fetchone()
        self.assertEqual(row['eligible_loads'],0)
        self.assertIsNone(row['noncompliance_pct'])
        row=self.db.execute("SELECT * FROM v_week_over_week WHERE week_start='2026-01-12' AND carrier='Carrier North'").fetchone()
        self.assertIsNotNone(row['prior_week_noncompliant'])

class TestEconomics(unittest.TestCase):
    def setUp(self):self.db=conn_for('carrier-economics-302')
    def tearDown(self):self.db.close()
    def test_no_revenue_multiplication(self):
        x=self.db.execute('SELECT COUNT(*) n,SUM(revenue) r FROM v_order_economics').fetchone()
        self.assertEqual((x['n'],x['r']),(4,4500))
    def test_extra_pay_aggregation(self):
        r=self.db.execute("SELECT extra_pay,total_carrier_cost,gross_margin FROM v_order_economics WHERE order_id='O-A'").fetchone()
        self.assertEqual((r['extra_pay'],r['total_carrier_cost'],r['gross_margin']),(55.,755.,245.))
    def test_missing_appointment_not_late(self):
        self.assertIsNone(self.db.execute("SELECT arrived_on_time FROM v_order_economics WHERE order_id='O-C'").fetchone()[0])
    def test_confirmation_grain(self):
        self.assertEqual(self.db.execute("SELECT rate_confirmation_count FROM v_order_economics WHERE order_id='O-B'").fetchone()[0],2)

class TestTracking(unittest.TestCase):
    def setUp(self):self.db=conn_for('trailer-tracking-addendum')
    def tearDown(self):self.db.close()
    def test_one_latest_row_per_asset(self):
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM v_asset_status').fetchone()[0],4)
        self.assertEqual(self.db.execute("SELECT event_id FROM v_latest_event WHERE asset_id='ASSET-A'").fetchone()[0],'E2')
    def test_no_future_order(self):
        self.assertEqual(self.db.execute("SELECT order_id FROM v_asset_asof_order WHERE asset_id='ASSET-A'").fetchone()[0],'ORD-1')
    def test_status_priority(self):
        s={r['asset_id']:r['business_status'] for r in self.db.execute('SELECT * FROM v_asset_status')}
        self.assertEqual(s,{'ASSET-A':'abandon_review','ASSET-B':'approved_hub','ASSET-C':'out_of_network','ASSET-D':'delayed'})

if __name__=='__main__':unittest.main()
