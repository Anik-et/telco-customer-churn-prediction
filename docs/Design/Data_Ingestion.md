# Data Ingestion Module

## Purpose

Read the raw dataset from disk and validate it before passing it to downstream modules.

---

## Responsibilities

- Read configuration
- Validate file existence
- Load CSV
- Validate schema
- Save processed copy
- Log all operations

---

## Inputs

- config.yaml
- CSV file

---

## Outputs

- Pandas DataFrame
- Processed CSV artifact

---

## Dependencies

- pandas
- pathlib
- yaml
- logger
- custom exceptions

---

## Error Handling

- Missing file
- Missing columns
- Empty dataset
- Invalid configuration

---

## Future Improvements

- SQL support
- AWS S3 support
- Azure Blob Storage
- Versioned datasets