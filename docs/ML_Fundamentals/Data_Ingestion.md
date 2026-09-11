# Data Ingestion

## Definition

Data ingestion is the process of collecting data from one or more sources and preparing it for downstream processing.

---

## Typical Data Sources

- CSV
- Excel
- SQL Databases
- APIs
- Cloud Storage
- Kafka

---

## Responsibilities

- Read data
- Validate source
- Validate schema
- Log operations
- Produce reproducible datasets

---

## Why separate data ingestion from preprocessing?

Data ingestion ensures the data is available and structurally correct.

Preprocessing transforms the data for machine learning.

Keeping these concerns separate makes systems easier to test, maintain, and extend.