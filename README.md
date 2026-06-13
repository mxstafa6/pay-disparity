# Profit vs Pay

A small data project looking at pay inequality inside large UK-listed companies.

I built this to explore a simple question: how has executive pay moved compared with typical employee pay inside large UK-listed companies? The starting point for this repo is UK pay-ratio disclosure data, especially CEO pay and employee pay bands. From there, I cleaned the dataset, filtered it down to companies with enough history to compare over time, and generated company-level charts showing how CEO pay has moved against median employee pay.

## What this project does

- Cleans raw UK pay disclosure data into analysis-ready CSV files.
- Keeps only companies with more than 4 years of usable pay records.
- Preserves CEO pay, lower quartile pay, median pay, upper quartile pay, and employee counts where available.
- Produces indexed pay charts so trends can be compared on the same scale.

## Current dataset

- `144` companies after filtering for usable history.
- `796` cleaned yearly observations.
- Coverage from `2019` to `2025`.
- Each company kept in the final cleaned data has at least `5` yearly rows.

## Why I chose indexed charts

Raw pay numbers are useful, but they can also hide the pace of change. Re-indexing both lines to `100` in the first available year makes the comparison much clearer:

- one line shows how CEO pay changes over time
- one line shows how median employee pay changes over time
- both start from the same baseline, so the divergence is easier to spot

That makes the charts more about trend and inequality than just absolute salary size.

## Repo structure

- `data/raw/`
  Raw source data.
- `data/cleaned/`
  Cleaned outputs, filtered company lists, and generated charts.
- `scripts/dataCleaner.py`
  Main cleaning pipeline for the pay dataset.
- `scripts/plotIndexedPayCharts.py`
  Chart generation script for indexed CEO vs median pay trends.

## What I worked on technically

- Data cleaning with `pandas`
- Column renaming and type conversion
- Handling missing values without losing useful company history
- Filtering by time-series coverage
- Exporting clean datasets for analysis and visualisation
- Automating chart generation across the full company set

## What I’d improve next

- Add a cleaner public-facing presentation layer, either as a notebook or a lightweight app.
- Add a small company selector so individual case studies are easier to browse.
- Write up a few standout company case studies instead of leaving the project as raw outputs alone.

## Files worth looking at

- [Cleaned wages data](data/cleaned/wages.csv)
- [Top companies file](data/cleaned/companies.csv)
- [Generated charts folder](data/cleaned/charts)
- [Data cleaning script](scripts/dataCleaner.py)
- [Chart script](scripts/plotIndexedPayCharts.py)

This repo is basically me using public company pay disclosures to turn a messy raw dataset into something easier to inspect, compare, and question.
