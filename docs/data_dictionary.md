# Data Dictionary

| Column | Description |
|---|---|
| Time | Seconds elapsed between each transaction and the first transaction in the dataset |
| V1 to V28 | PCA-transformed anonymized transaction features |
| Amount | Transaction amount |
| Class | Target variable where 1 means fraud and 0 means non-fraud |

## Notes
The dataset is anonymized for privacy. Most original transaction fields are transformed into PCA components.
