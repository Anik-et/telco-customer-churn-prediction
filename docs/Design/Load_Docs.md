# Load Data Module

## Purpose

Loads the raw customer churn dataset.

---

## Input

CSV file location from config.yaml

---

## Output

Pandas DataFrame

---

## Responsibilities

Read configuration.

Validate path.

Read CSV.

Return DataFrame.

---

## Why separate module?

Keeps data loading independent from preprocessing and model training.

Allows replacing CSV with SQL or S3 in the future without modifying downstream code.