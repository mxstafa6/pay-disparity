# Pay Disparity

An analysis of CEO pay versus median employee pay across UK energy and utilities companies from `2019` to `2025`.

Using public UK pay-ratio disclosures, this project cleans company-level pay data, filters it to energy-related firms, and compares how executive pay and worker pay moved over time. Both series are re-indexed to `100` in the first available year so the charts show change in pace, not just differences in salary size.

## Key findings

- **Centrica** shows the sharpest divergence in the sample. Indexed CEO pay rose by roughly `264%` from `2019` to `2024`, while indexed median pay rose by about `35%`.
- **Drax** also shows a clear split. CEO pay rose by roughly `146%`, compared with median pay growth of about `65%`.
- The pattern is not universal. **BP** and **Royal Dutch Shell** show cases where median employee pay rose while indexed CEO pay ended below its own starting point.

The result is a mixed picture rather than a one-note one. Some firms show a sharp split between executive and worker pay growth, while others do not.

## Sample charts

![BP](data/cleaned/charts/bp_indexed_pay.png)
![Centrica](data/cleaned/charts/centrica_indexed_pay.png)
![Drax](data/cleaned/charts/drax_indexed_pay.png)

## Dataset

- `10` companies after sector and history filtering
- `58` yearly observations
- `2019` to `2025` coverage
- Source data from UK mandatory pay-ratio disclosures
- Final sample limited to firms with at least `5` yearly observations

## Why use indexed charts?

Raw salary levels are not very useful for cross-company comparison on their own. Re-indexing both CEO pay and median employee pay to `100` in the first available year makes the charts easier to read:

- a line ending at `150` means pay is `50%` above its starting point
- a line ending at `80` means pay is `20%` below its starting point
- the distance between the two lines shows whether executive compensation and worker pay moved together or drifted apart

## Approach

1. Clean the raw disclosure dataset with `pandas`
2. Filter it to UK energy and utility-related firms
3. Keep only companies with enough yearly history to compare over time
4. Generate indexed CEO-versus-median-pay charts with `matplotlib`

## Stack

Python, pandas, matplotlib

## Project files

- [analysis.ipynb](analysis.ipynb) — notebook version of the project story
- [scripts/dataCleaner.py](scripts/dataCleaner.py) — cleaning and filtering pipeline
- [scripts/plotIndexedPayCharts.py](scripts/plotIndexedPayCharts.py) — chart generation script
- [data/cleaned/wages.csv](data/cleaned/wages.csv) — cleaned yearly pay data
- [data/cleaned/companies.csv](data/cleaned/companies.csv) — filtered company list
- [data/cleaned/charts](data/cleaned/charts) — generated company charts
