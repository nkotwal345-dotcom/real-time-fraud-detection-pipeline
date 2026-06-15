from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

DATA_PATH = Path('data/creditcard.csv')
REPORTS_DIR = Path('reports')
IMAGES_DIR = Path('images')
REPORTS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = [c.lower() for c in df.columns]
for col in df.columns:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(chr(39), '', regex=False).str.replace(chr(34), '', regex=False).str.strip(), errors='coerce')
df = df.dropna().reset_index(drop=True)
df['class'] = df['class'].astype(int)

total_transactions = len(df)
fraud_transactions = int((df['class'] == 1).sum())
fraud_rate = round((df['class'] == 1).mean() * 100, 4)
total_fraud_amount = round(df.loc[df['class'] == 1, 'amount'].sum(), 2)
avg_fraud_amount = round(df.loc[df['class'] == 1, 'amount'].mean(), 2)
avg_nonfraud_amount = round(df.loc[df['class'] == 0, 'amount'].mean(), 2)

kpis = pd.DataFrame([
    {'metric': 'Total Transactions', 'value': total_transactions},
    {'metric': 'Fraud Transactions', 'value': fraud_transactions},
    {'metric': 'Fraud Rate Percentage', 'value': fraud_rate},
    {'metric': 'Total Fraud Amount', 'value': total_fraud_amount},
    {'metric': 'Average Fraud Amount', 'value': avg_fraud_amount},
    {'metric': 'Average Non-Fraud Amount', 'value': avg_nonfraud_amount}
])
kpis.to_csv(REPORTS_DIR / 'fraud_kpis.csv', index=False)

class_counts = df['class'].value_counts().sort_index()
plt.figure(figsize=(8, 5))
class_counts.plot(kind='bar')
plt.title('Fraud vs Non-Fraud Transaction Count')
plt.xlabel('Class: 0 = Non-Fraud, 1 = Fraud')
plt.ylabel('Transaction Count')
plt.tight_layout()
plt.savefig(IMAGES_DIR / 'fraud_class_distribution.png')
plt.close()

amount_cap = df['amount'].quantile(0.99)
plt.figure(figsize=(8, 5))
df[df['amount'] <= amount_cap]['amount'].hist(bins=50)
plt.title('Transaction Amount Distribution - Capped at 99th Percentile')
plt.xlabel('Transaction Amount')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig(IMAGES_DIR / 'transaction_amount_distribution.png')
plt.close()

X = df.drop(columns=['class'])
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
y_score = model.predict_proba(X_test_scaled)[:, 1]

precision = round(precision_score(y_test, y_pred), 4)
recall = round(recall_score(y_test, y_pred), 4)
f1 = round(f1_score(y_test, y_pred), 4)
roc_auc = round(roc_auc_score(y_test, y_score), 4)
cm = confusion_matrix(y_test, y_pred)

metrics = pd.DataFrame([
    {'metric': 'Precision', 'value': precision},
    {'metric': 'Recall', 'value': recall},
    {'metric': 'F1 Score', 'value': f1},
    {'metric': 'ROC AUC', 'value': roc_auc}
])
metrics.to_csv(REPORTS_DIR / 'model_metrics.csv', index=False)

summary_lines = [
    '# Fraud Analysis Report',
    '',
    '## Dataset Summary',
    f'- Total transactions: {total_transactions:,}',
    f'- Fraud transactions: {fraud_transactions:,}',
    f'- Fraud rate: {fraud_rate}%',
    f'- Total fraud amount: ',
    f'- Average fraud amount: ',
    '',
    '## Model Performance',
    f'- Precision: {precision}',
    f'- Recall: {recall}',
    f'- F1 Score: {f1}',
    f'- ROC AUC: {roc_auc}',
    '',
    '## Business Interpretation',
    'The dataset is highly imbalanced, which is common in fraud analytics. Recall is important because fraud teams want to capture as many fraudulent transactions as possible, while precision helps control false positives and operational review volume.',
    '',
    '## Generated Outputs',
    '- reports/fraud_kpis.csv',
    '- reports/model_metrics.csv',
    '- images/fraud_class_distribution.png',
    '- images/transaction_amount_distribution.png'
]
Path('reports/fraud_analysis_report.md').write_text('\n'.join(summary_lines), encoding='utf-8')

print('Fraud analysis completed successfully.')
print(kpis)
print(metrics)

