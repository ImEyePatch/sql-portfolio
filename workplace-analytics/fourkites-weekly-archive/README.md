# FourKites Weekly Compliance Report Archive // public workflow reconstruction

An offline, provider-neutral reproduction of the weekly email-to-archive processing pattern. The source flow includes an XLSX attachment filter, a report date range and composed week boundaries, nested folder checks, and replace/create actions. This public example accepts an explicit synthetic week range and uses local folders.

**Implementation:** `tools/archive_simulator.py`; see `docs/flow-logic.md` and `flows/public-blueprint.json`. From package root: `python -m unittest discover -s tests -v`.

The original connector bindings, mailbox details, SharePoint folder structure and expressions are intentionally not published.
