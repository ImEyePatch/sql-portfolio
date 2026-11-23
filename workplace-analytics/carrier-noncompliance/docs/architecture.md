# Operational non-compliance / public architecture

```mermaid
flowchart LR
  A[Weekly tracking snapshots] --> D[Deduplicate by load + week]
  B[Load reference] --> E[Carrier and lane enrichment]
  C[Geofence observations] --> F[Event quality audit]
  D --> E
  E --> G[No-movement exclusions]
  G --> H[Geofence / ping classification]
  H --> I[Weekly carrier and lane KPIs]
```

**Source review:** supplied `Compliance.zip` includes `NonCompliance`, `fact_DailyGeofence`, 21 measures, 18 relationships, 12 pages (including definition/tooltips), and transformations joining load data with operational tables. Its named failure types include geofence and ping frequency; a no-movement exclusion appears explicitly.

**Synthetic implementation choices:** the 30-minute ping threshold is invented for demonstration. Original business thresholds, vendor records, and source paths are not reproduced. The weekly table grain is load-per-week after deterministic deduplication. For actual reporting, verify how snapshot precedence is defined. Counts across failure categories overlap only in explicit `both`; summing geofence and ping failure counts is not a valid estimate of total noncompliant loads.

**Pages to rebuild with synthetic charts:** overview, carrier overview, detailed load classification, failed-lane ranking, week-over-week trend, and six brief metric-definition tooltips.
