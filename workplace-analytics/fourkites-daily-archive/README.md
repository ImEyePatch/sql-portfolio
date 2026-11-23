# FourKites Daily Geofence Report Archive // public workflow reconstruction

An offline, provider-neutral reproduction of an email-to-archive processing pattern observed in the daily Power Automate export. Does not connect to the original mailbox or SharePoint. Uses fictional attachments and creates a local `daily/YYYY/MM` archive.

**Source-derived stages:** shared-mailbox trigger; XLS filter; report date; year/month folder checks; get attachment; replace/create file. **Independent implementation:** `tools/archive_simulator.py`, with path safety, deterministic write outcomes, idempotency and unit tests.

From package root: `python -m unittest discover -s tests -v`. See `docs/flow-logic.md` and `flows/public-blueprint.json`.
