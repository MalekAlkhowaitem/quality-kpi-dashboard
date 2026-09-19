# Quality KPI Dashboard

A Python script that builds a one-page quality dashboard: First Pass Yield (FPY), Cost of Poor Quality (COPQ), defects by type and a Pareto of defect causes.

All data in this repository is **synthetic**. No employer or client data is used.

## What it shows
- **First Pass Yield** by month against a 95% target
- **Cost of Poor Quality** split into failure, appraisal and prevention cost
- **Defects by type**, stacked by month
- **Pareto chart** of defect types with cumulative percentage

## Run it
```bash
pip install numpy matplotlib
python kpi_dashboard.py
```

Output: `quality_kpi_dashboard.png` and a printed FPY / COPQ summary.

## Example result (synthetic data)
FPY improves from about 91% in January to about 96% in December while COPQ falls, the pattern you would expect when prevention spend rises and rework falls.

## Adapting it
Replace `make_data()` with your own monthly figures (units produced, defects, cost categories, defect types). The chart code does not change.

## Metric definitions
- **FPY** = (units - defective units) / units
- **COPQ** = internal and external failure cost + appraisal cost + prevention cost
- **Pareto** = defect types ranked by count, with cumulative percentage line

Author: Malek Alkhowaitem, Quality Director (ISO 9001:2015 Lead Auditor, Lean Six Sigma Black Belt)
