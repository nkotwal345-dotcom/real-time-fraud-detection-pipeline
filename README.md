# Real-Time Fraud Detection Pipeline

## Project Overview
This project builds a near-real-time fraud detection analytics pipeline using real anonymized credit card transaction data, SQL, Python, anomaly detection, and BI reporting.

## Business Problem
Financial institutions process large transaction volumes every day. Fraud and risk teams need faster ways to identify suspicious transactions, monitor fraud patterns, reduce false positives, and support operational decision-making.

## Dataset
This project uses the Credit Card Fraud Detection dataset from Kaggle.

The dataset contains anonymized credit card transactions made by European cardholders in September 2013. It includes 284,807 transactions, with 492 fraud transactions, making it a highly imbalanced fraud detection dataset.

Dataset file to download locally:
creditcard.csv

Important: Raw data is not pushed to GitHub. Only documentation, code, SQL, and analysis outputs are committed.

## Tools and Technologies
- Python
- Pandas
- NumPy
- Scikit-learn
- SQL
- Matplotlib
- Power BI or Tableau
- GitHub

## Project Workflow
1. Download and store the dataset locally
2. Clean and validate transaction records
3. Analyze fraud vs non-fraud transaction patterns
4. Engineer fraud risk features
5. Build fraud monitoring SQL queries
6. Apply anomaly detection and classification models
7. Create dashboard KPIs for fraud operations
8. Summarize business insights and recommendations

## Key Business KPIs
- Total transaction volume
- Fraud transaction count
- Fraud rate
- Fraud amount exposure
- Average fraud transaction amount
- High-value transaction risk
- Fraud detection precision and recall
- False positive review volume

## Repository Structure
- data: dataset instructions only
- notebooks: Python analysis notebooks
- sql: fraud monitoring SQL queries
- src: reusable Python scripts
- dashboards: dashboard requirements and screenshots
- reports: final business summary
- docs: data dictionary and documentation
- images: charts and dashboard screenshots

## Business Impact
This project demonstrates how fraud analytics can help risk teams identify suspicious activity, prioritize high-risk transactions, and support faster operational review.

## Status
Project foundation created. Next steps include dataset download, EDA notebook, model development, dashboard screenshots, and final project report.
