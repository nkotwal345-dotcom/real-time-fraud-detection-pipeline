from pathlib import Path
import pandas as pd

DATA_PATH = Path('data/creditcard.csv')
REPORTS_DIR = Path('reports')
REPORTS_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = [c.lower() for c in df.columns]

for col in df.columns:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(chr(39), '', regex=False).str.replace(chr(34), '', regex=False).str.strip(), errors='coerce')

df = df.dropna().reset_index(drop=True)

feature_cols = [c for c in df.columns if c.startswith('v')]
df['anomaly_score'] = df[feature_cols].abs().mean(axis=1)
df['amount_score'] = (df['amount'] - df['amount'].min()) / (df['amount'].max() - df['amount'].min())
df['anomaly_score_scaled'] = (df['anomaly_score'] - df['anomaly_score'].min()) / (df['anomaly_score'].max() - df['anomaly_score'].min())
df['fraud_risk_score'] = (0.7 * df['anomaly_score_scaled']) + (0.3 * df['amount_score'])

alert_threshold = df['fraud_risk_score'].quantile(0.99)
df['alert_flag'] = (df['fraud_risk_score'] >= alert_threshold).astype(int)

alerts = df[df['alert_flag'] == 1].copy()
alerts = alerts.sort_values('fraud_risk_score', ascending=False)
alerts[['time', 'amount', 'fraud_risk_score', 'class']].head(100).to_csv(REPORTS_DIR / 'fraud_alerts_sample.csv', index=False)

summary = pd.DataFrame([
    {'metric': 'Total Transactions Scored', 'value': len(df)},
    {'metric': 'Alert Threshold Percentile', 'value': '99th percentile'},
    {'metric': 'Generated Alerts', 'value': int(df['alert_flag'].sum())},
    {'metric': 'Fraud Cases Inside Alerts', 'value': int(alerts['class'].sum())},
    {'metric': 'Alert Fraud Capture Rate Percentage', 'value': round(100 * alerts['class'].sum() / df['class'].sum(), 2)}
])

summary.to_csv(REPORTS_DIR / 'alert_summary.csv', index=False)

print('Near-real-time fraud alert simulation completed successfully.')
print(summary)
