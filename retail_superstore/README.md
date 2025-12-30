# Retail Superstore Analytics: Power BI Portfolio Project

### End-to-end data exploration, profitability diagnostics, and customer value analysis

This project analyzes the classic Retail Superstore dataset to identify revenue patterns, margin leakage, discount sensitivity, and high-value customer segments.
It demonstrates capability across data cleaning, exploratory analysis, Power BI modeling, DAX metric development, and business-focused insight generation.

The work was completed to form part of a data analytics portfolio suitable for review by IT and Data leadership.

---

## Project Overview

| Aspect    | Summary                                                                         |
| --------- | ------------------------------------------------------------------------------- |
| Objective | Diagnose revenue and profitability drivers to support strategic decision-making |
| Dataset   | Superstore — approximately 10,000 orders, spanning four years                   |
| Tools     | Python (EDA), Power BI (visualization and modeling), DAX, GitHub                |
| Output    | Multi-page Power BI dashboard and written insights aligned to executive needs   |

---

## Repository Structure

```
├── data/
│   └── superstore.csv
├── notebooks/
│   └── 01_eda.ipynb
├── dashboards/
│   ├── executive_overview.png
│   ├── profitability_drivers.png
│   └── customer_value_segmentation.png
├── retail_superstore.pbix
└── README.md
```

---

## Analytical Focus Areas

* Revenue and seasonality trends
* Drivers of profit and margin erosion
* Impact of discounting on profitability
* Product-level margin leakage
* Customer lifetime value estimation and segmentation

---

# Executive Summary of Insights

### 1. Regional concentration drives performance

The East and West regions account for the majority of total revenue and profit.
The Central and Midwest regions contribute significantly less, indicating an opportunity for geographic expansion and targeted market development.

### 2. Discounting directly impacts margin performance

Discounts greater than approximately 30 percent consistently eliminate profit, regardless of volume contribution.
Nearly all positive profit is generated within the 0–10 percent discount range.
This suggests discount policy is a significant margin lever.

### 3. Losses originate from a defined set of SKUs

Specific product types such as binding systems, chair products, paper goods, and envelopes repeatedly show negative or minimal margin.
These products are strong candidates for price adjustment, vendor renegotiation, or discontinuation.

### 4. Customer retention is exceptionally strong

The repeat purchase rate is approximately 98 percent, indicating reliable recurring revenue and strong customer loyalty.
As a result, retention-focused strategies may be more efficient than new customer acquisition.

### 5. Customer value distribution follows a Pareto pattern

A small subset of customers contributes disproportionately to overall lifetime value.
Corporate customers in particular show higher profit per customer relative to other segments.

---

# Dashboard Pages


### Executive Overview

`/dashboards/executive_overview.png`

### Profitability Drivers

`/dashboards/profitability_drivers.png`

### Customer Value and Segmentation

`/dashboards/customer_value_segmentation.png`

---

# Core DAX Measures Used

```DAX
Total Sales = SUM('superstore'[Sales])

Total Profit = SUM('superstore'[Profit])

Total Orders = DISTINCTCOUNT('superstore'[Order ID])

Total Customers = DISTINCTCOUNT('superstore'[Customer ID])

Sales per Customer =
DIVIDE([Total Sales], [Total Customers], 0)

Profit per Customer =
DIVIDE([Total Profit], [Total Customers], 0)

Average Order Value (AOV) =
DIVIDE([Total Sales], [Total Orders], 0)

Repeat Purchase Rate = 
VAR CustomersTable =
    SUMMARIZE(
        'superstore',
        'superstore'[Customer ID],
        "OrderCount", DISTINCTCOUNT('superstore'[Order ID])
    )
VAR RepeatCustomers =
    COUNTROWS(
        FILTER(CustomersTable, [OrderCount] > 1)
    )
VAR TotalCustomers =
    DISTINCTCOUNT('superstore'[Customer ID])
RETURN
DIVIDE(RepeatCustomers, TotalCustomers, 0)

Customer Lifetime Value (CLV) =
[Profit per Customer] + ( [Average Order Value (AOV)] * [Repeat Purchase Rate] )
```

---

# Recommendations

| Finding                                            | Recommended Action                                                 | Expected Outcome                                      |
| -------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------- |
| Margin erosion at discount levels above 30%        | Set discount approval thresholds and automate discount limits      | Margin protection without major volume loss           |
| SKU-level losses concentrated in specific products | Evaluate pricing adjustments, renegotiate costs, or discontinue    | Immediate improvement in portfolio profitability      |
| Underperformance in Central and Midwest regions    | Targeted expansion strategy and demand testing                     | Revenue diversification and growth                    |
| High customer retention rate                       | Invest in loyalty and value-added services rather than acquisition | Increased lifetime value at lower cost                |
| High-value corporate customers                     | Expand corporate sales programs and bulk pricing                   | Higher transaction value and stable recurring revenue |

---

# Next Steps

* Develop discount elasticity models by category
* Implement churn and retention-based CLV modeling if time-series customer behavior data becomes available
* Expand dashboard to include cohort analysis and customer trend monitoring
* Automate data ingestion and scheduling for continuous reporting

---

# Contact

For further discussion or access to the live report:

**Samuel Head**
Data & Business Analytics
GitHub: ImEyePatch

---

# Status

| Component             | Status                  |
| --------------------- | ----------------------- |
| EDA completed         | Yes                     |
| Power BI development  | Completed (three pages) |
| Insights documented   | Completed               |
| Portfolio publication | In progress             |
