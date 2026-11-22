# Workplace BI case studies

> These summaries document technical work without publishing employer source code or private data. They are draft portfolio descriptions requiring confidentiality review.

## USPS At-a-Glance / Service Reconciliation

**Problem:** Operational event timestamps, report scopes, and exemption decisions can produce different on-time service calculations.

**Approach:** Traced report lineage, verified order and event matching, checked origin/destination stop selection, compared scheduled and actual timestamps, analyzed approved versus pending adjudications, and designed lane and carrier drilldowns. Used SQL, DAX, and Power BI to investigate scoring denominators and matching gaps.

**Evidence from supplied archive:** Pages include USPS At-A-Glance, USPS Service Reconciliation, USPS Pending Scenarios, USPS Lane Scoreboard, and Postal Timestamp Audit. The project includes service and lane-oriented DAX measures.

**Limit:** A report page's presence does not independently establish every metric was validated or deployed.

## Non-Compliance / Carrier Performance

**Problem:** Tracking failures needed to be categorized and explained by carrier, lane, and week.

**Approach:** Built carrier and overall views using geofence failures, ping-frequency failures, affected loads, carrier concentration, and week-over-week change measures. Added tooltip-specific definitions and detailed drilldowns.

**Evidence:** The supplied Power BI project contains NonCompliance Overview, Carrier Overview, NonCompliance Detail, plus tooltip pages and DAX measures for failure counts and concentration.

## FourKites Daily and Weekly Archive Automation

**Problem:** Excel email attachments needed predictable historical archives for downstream reporting.

**Approach:** Used shared-mailbox triggers, file-extension filtering, date-based naming, year/month folder checks, and per-attachment processing. The exported daily flow processes XLS attachments; the weekly flow processes XLSX attachments and composes week-start/end metadata.

**Limit:** The definitions were inspected; actual execution success rates were not measured.

## Database Migration and Trailer Tracking

**Problem:** A legacy reporting model required reliable new-database mappings and defensible current-asset lookups.

**Approach:** Audited key coverage, field population, stop chronology, missing references, and conditional classifications; documented alternative SQL and Power Query patterns.

**Public companion:** [Trailer Tracking Power BI — sanitized reconstruction](https://github.com/ImEyePatch/trailer-tracking-powerbi).

## 302 / Carrier Economics

**Focus:** Carrier charges, trip duration, route schedule reference tables, and on-time trip/service measures.

**Evidence:** Uploaded 302 project archive includes Power BI analysis pages, carrier-pay and driver-extra-pay tables, and trip metrics.

---

**Publishing rule:** Never copy production PBIP/PBIX exports, flow definitions, internal SQL, credentials, customer names, tracking events, or restricted source data to a public repository without explicit written employer permission. Use independently authored, synthetic demonstrations instead.
