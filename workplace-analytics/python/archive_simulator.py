"""Offline, vendor-neutral file archiver. All example attachments are synthetic.

This is not a Power Automate connector. It models idempotent create/replace,
folder partitioning, and extension checks visible in the supplied flows.
"""
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
import re, tempfile, os, hashlib

@dataclass(frozen=True)
class Attachment:
    filename: str
    data: bytes


def _safe_name(filename: str, required_suffix: str):
    if Path(filename).name != filename or filename in ('', '.', '..') or '/' in filename or '\\' in filename:
        raise ValueError('Filename must be a single safe basename')
    if not filename.lower().endswith(required_suffix):
        raise ValueError('Unexpected attachment extension')
    if not re.fullmatch(r'[A-Za-z0-9_. -]+', filename):
        raise ValueError('Filename contains unsupported characters')
    return filename


def archive_daily(root: Path, report_date: date, items: Iterable[Attachment]):
    """Save eligible *.xls attachments under a dated folder.

    An XLS extension is checked; this does NOT validate file content.
    No original report attachment is needed or opened by this demo.
    """
    dest = Path(root) / 'daily' / f'{report_date.year:04d}' / f'{report_date.month:02d}'
    return _archive(dest,items,'.xls')


def archive_weekly(root: Path, week_start: date, week_end: date, items: Iterable[Attachment]):
    """Save synthetic *.xlsx files for a specified seven-day reporting week."""
    if (week_end-week_start).days!=6:
        raise ValueError('Week start and end must cover exactly seven calendar dates')
    dest = Path(root) / 'weekly' / f'{week_start.year:04d}' / f'{week_start.month:02d}'
    return _archive(dest,items,'.xlsx',prefix=f'{week_start:%Y%m%d}_{week_end:%Y%m%d}_')


def _archive(dest: Path, items: Iterable[Attachment], suffix: str, prefix: str=''):
    outputs=[]
    valid=[]
    for item in items:
        if not item.filename.lower().endswith(suffix):
            continue
        name=_safe_name(item.filename,suffix)
        valid.append((name,item.data))
    if not valid:
        return outputs
    dest.mkdir(parents=True,exist_ok=True)
    for name,data in valid:
        file=dest/(prefix+name)
        digest=hashlib.sha256(data).hexdigest()
        existed=file.exists()
        if existed and hashlib.sha256(file.read_bytes()).hexdigest()==digest:
            action='unchanged'
        else:
            temp=None
            try:
                with tempfile.NamedTemporaryFile(dir=dest,delete=False) as f:
                    f.write(data);temp=f.name
                os.replace(temp,file)
                action='replaced' if existed else 'created'
            finally:
                if temp and os.path.exists(temp):os.unlink(temp)
        outputs.append({'filename':file.name,'action':action,'sha256':digest,'relative_path':str(file.relative_to(dest.parent.parent.parent))})
    return outputs
