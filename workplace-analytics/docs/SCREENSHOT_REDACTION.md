# Screenshots: how to capture Power BI pages safely

**Best option:** make a copy of the report for portfolio use, replace every query's source with synthetic data (or rebuild the layout in a clean report) and screenshot that version. Simply clearing credentials or using "Edit interactions" does **not** remove imported data from the PBIX. Do not upload the production PBIX or an exported PDF with real data.

## Quick screenshot workflow when no synthetic report exists
1. In Power BI Desktop open the report, navigate to the page, and fit it to the canvas. Turn off any sensitive browser tabs or UI overlays.
2. Use the screenshot shortcut (`Win` + `Shift` + `S` on Windows) to capture only the report canvas. Do not include the field list or queries/data preview.
3. Before sharing, **cover** all table rows, charts, KPI numbers, tooltip values, names, order IDs, routes, timestamps, financial amounts, and the filter pane if it contains sensitive values. Use solid opaque filled rectangles in an image editor, not a light blur or transparent highlighter. Crop out titles if they contain confidential names.
4. Save as a new flattened PNG; reopen it and check at full zoom. Also inspect image metadata for information you do not want to share.
5. For a polished public case study, reproduce the chart with synthetic values rather than publishing a heavily redacted screenshot. Label it `Synthetic illustrative dashboard`.

## What I can do with your screenshots
Upload one image per report page. I can help identify all sensitive locations, remove/cover the data with fully opaque redactions or generate a clean portfolio mockup with synthetic values while preserving the layout. The source screenshots should remain private, and only the fully reviewed reconstructions should be published.
