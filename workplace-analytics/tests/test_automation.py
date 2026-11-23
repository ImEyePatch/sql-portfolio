import sys
from datetime import date
from pathlib import Path
import tempfile,unittest
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'tools'))
from archive_simulator import archive_daily, archive_weekly, Attachment

class TestDailyArchive(unittest.TestCase):
    def setUp(self):self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name)
    def tearDown(self):self.t.cleanup()
    def test_extension_and_path_and_idempotency(self):
        results=archive_daily(self.root,date(2026,1,2),[Attachment('report.xls',b'synthetic'),Attachment('other.pdf',b'bad')])
        self.assertEqual(len(results),1)
        path=self.root/'daily/2026/01/report.xls'
        self.assertEqual(path.read_bytes(),b'synthetic')
        self.assertEqual(archive_daily(self.root,date(2026,1,2),[Attachment('report.xls',b'synthetic')])[0]['action'],'unchanged')
        self.assertEqual(archive_daily(self.root,date(2026,1,2),[Attachment('report.xls',b'updated')])[0]['action'],'replaced')
        with self.assertRaises(ValueError):archive_daily(self.root,date(2026,1,2),[Attachment('../attack.xls',b'bad')])
    def test_empty(self):
        self.assertEqual(archive_daily(self.root,date(2026,1,2),[Attachment('none.xlsx',b'test')]),[])

class TestWeeklyArchive(unittest.TestCase):
    def setUp(self):self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name)
    def tearDown(self):self.t.cleanup()
    def test_period_boundary(self):
        result=archive_weekly(self.root,date(2025,12,29),date(2026,1,4),[Attachment('weekly.xlsx',b'synthetic')])
        self.assertEqual(len(result),1)
        self.assertTrue((self.root/'weekly/2025/12/20251229_20260104_weekly.xlsx').exists())
    def test_bad_range(self):
        with self.assertRaises(ValueError):archive_weekly(self.root,date(2026,1,1),date(2026,1,5),[Attachment('weekly.xlsx',b'a')])
    def test_skip_wrong_extension(self):
        self.assertEqual(archive_weekly(self.root,date(2026,1,5),date(2026,1,11),[Attachment('file.xls',b'data')]),[])

if __name__=='__main__':unittest.main()
