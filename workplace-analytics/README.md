# SAMUEL HEAD // DATA SYSTEMS PORTFOLIO — RECONSTRUCTION WORKSPACE

```text
+--------------------------------------------------------------------------+
|  S A M U E L  H E A D                             PUBLIC-ONLY / 2026     |
|--------------------------------------------------------------------------|
|  SQL SERVER  /  SQLITE  /  DAX  /  POWER QUERY  /  POWER BI /  PYTHON     |
|  INPUT      SIX USER-SUPPLIED PROJECT EXPORTS                            |
|  OUTPUT     SYNTHETIC REPRODUCTIONS + TESTS + CASE STUDIES               |
|  SECURITY   NO PRODUCTION CODE OR DATA IN THIS PACKAGE                    |
+--------------------------------------------------------------------------+
```

This is an **independently reconstructed portfolio workspace** for six actual project *types* investigated in source archives. Each folder contains technical notes, sample data or workflow blueprints, and executable/query examples. The source files were not copied into the public workspace; actual production formulas and internal connection details are retained only in a **separately marked confidential reference**.

## Projects

| Folder | Technical scope | Code and evidence |
|---|---|---|
| [USPS service reconciliation](usps-service-reconciliation/) | Event scoring, event-to-event comparison, unique approved exclusions, pending simulations, lane/carrier reporting | SQL + 3 DAX modules + M + data + tests |
| [Carrier non-compliance](carrier-noncompliance/) | Weekly geofence/ping failures, no-movement exclusion, carrier/lane concentration | SQL + DAX + M + data + tests |
| [Carrier economics (302)](carrier-economics-302/) | Order-grain financial enrichment, extra pay, rate confirmations, on-time performance | SQL + DAX + M + data + tests |
| [Trailer tracking addendum](trailer-tracking-addendum/) | Deterministic latest event, as-of order matching, business status classification | SQL + DAX + M + data + tests |
| [Daily report archive](fourkites-daily-archive/) | Shared-mailbox daily XLS classification, year/month archive, replace/create | Flow blueprint + offline Python + tests |
| [Weekly report archive](fourkites-weekly-archive/) | XLSX filtering, week start/end, year/month partition, replace/create | Flow blueprint + offline Python + tests |

The existing public [Trailer Tracking Power BI](https://github.com/ImEyePatch/trailer-tracking-powerbi) repository remains the deeper primary case study for that system. The tracking folder here is an additive validation example.

## Quick start

Requires **Python 3.9+**. For the SQL, synthetic data generator, and unit tests, no third-party packages, secrets, servers or paid services are needed.

```bash
python tools/generate_synthetic.py
python -m unittest discover -s tests -v
python tools/run_query_examples.py usps-service-reconciliation
python tools/run_query_examples.py carrier-noncompliance
python tools/run_query_examples.py carrier-economics-302
python tools/run_query_examples.py trailer-tracking-addendum
```

The simulator for email-attachment archiving is in `tools/archive_simulator.py` and is covered by the same tests. The files inside each `power-query/` directory can be adapted to Power BI's blank-query Advanced Editor using a `pDataRoot` text parameter pointing to that project's `data/` folder. The `.dax` files are **measure blueprints**: add measures one at a time to the imported tables with matching names. They have not been run in the Power BI DAX engine.

## Documentation

- [Source review coverage](docs/SOURCE_COVERAGE.md)
- [Screenshot removal and redaction](docs/SCREENSHOT_REDACTION.md)
- [Report-by-report screenshot plan](docs/REPORT_PAGE_PLANS.md)
- [Release requirements](docs/RELEASE_CHECKLIST.md)
- [GitHub repository rollout](docs/GITHUB_DEPLOYMENT_PLAN.md)
- [Publication and data security policy](SECURITY.md)

## What this project proves—and what it does not

**Demonstrated locally:** SQL schema/view composition, synthetic dataset creation, event matching/exemption logic, week-by-week compliance calculations, join-grain protection for economics, latest/as-of asset logic, file-archive idempotency, path validation, and automated tests.

**Not yet demonstrated:** successful Power BI project rebuild, tested production connections, original employer code equivalence, production deployment, original Power Automate execution history, or publication permission. Do not claim those outcomes from this reconstruction.

The end result should be a recruiter-friendly GitHub portfolio, with real engineering reasoning visible in the public-safe example code. Styling is intentionally ASCII/terminal-inspired but kept restrained for readability.

## No-data report gallery

These are **redrawn/edited presentation mockups**, not functioning Power BI reports or production exports. All report numbers and record values were removed. Employer-associated branding, layout and terminology still require permission review.

| Report | Screenshots | Focus |
|---|---|---|
| [USPS At-a-Glance](usps-service-reconciliation/assets/screenshots/README.md) | 6 | Network scoring, OTP tooltip, carrier performance, adjudication scenarios, lane scoreboard and reconciliation |
| [Non-Compliance](carrier-noncompliance/assets/screenshots/README.md) | 4 | Network overview, carrier analysis, load details, flagged-load tooltip |
| [302 Carrier Economics](carrier-economics-302/assets/screenshots/README.md) | 1 | Trip and service detail table |
| [Trailer Tracking](trailer-tracking-addendum/assets/screenshots/README.md) | 1 | Location and status dashboard |

**Total:** 12 blank-data screenshot mockups. The images illustrate page structure only; they do not validate the independently reconstructed SQL, DAX, or Power Query implementations.
