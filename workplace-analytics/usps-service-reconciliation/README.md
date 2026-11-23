# USPS Service Reconciliation // synthetic technical reconstruction

> **Public portfolio version.** Inspired by an internal Power BI reporting project reviewed from `Glance(9).zip`. No production query, dataset, or PBIP file is included.

## The business problem
Reconcile operational arrival/departure performance across two reporting systems where mismatched event timestamps, scoring eligibility, adjudication outcomes, and lane scope can alter KPI results.

## What is implemented
- SQL schema + event-reconciliation view (`sql/10_event_reconciliation.sql`)
- Unique event-level adjudication audit (`sql/20_adjudication_audit.sql`)
- Before/after/pending scenarios, lane scoreboards, carrier disagreements (`sql/30_kpis.sql`)
- DAX measure blueprint, Power Query CSV import, synthetic data generator, and executable unit tests
- Architecture and quality-gate documentation (`docs/architecture.md`)

## Dashboard page screenshots (no data)

The [six-page screenshot gallery](assets/screenshots/README.md) documents the visual design: a network overview, OTP explanation tooltip, carrier performance, adjudication scenarios, lane scoreboard, and event-level service reconciliation.

[![Blank-data USPS-style reporting overview](assets/screenshots/01-at-a-glance-overview.png)](assets/screenshots/01-at-a-glance-overview.png)

**Important:** These are edited presentation mockups with the metrics, dates and table records removed. They are not live outputs of the synthetic demo. Corporate branding and business-logic terminology require permission review before publishing.

## Reproduce
From the package root: `python tools/generate_synthetic.py` then `python -m unittest discover -s tests -v`. For an exploratory SQL run: `python tools/run_query_examples.py usps-service-reconciliation`.

**Interpretation warning:** sample output is invented, so sample rates are not actual service results. DAX and Power Query files are example patterns requiring manual integration and validation in Power BI; SQL examples are executed in the test suite.
