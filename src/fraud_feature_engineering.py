import pandas as pd

def load_transactions(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.lower() for col in df.columns]
    df = df.drop_duplicates()
    return df

def create_fraud_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['high_value_transaction'] = (df['amount'] > df['amount'].quantile(0.95)).astype(int)
    df['amount_z_score'] = (df['amount'] - df['amount'].mean()) / df['amount'].std()
    df['high_amount_outlier'] = (df['amount_z_score'].abs() > 3).astype(int)
    return df

def summarize_fraud_kpis(df: pd.DataFrame) -> dict:
    return {
        'total_transactions': int(len(df)),
        'fraud_transactions': int(df['class'].sum()),
        'fraud_rate_percentage': round(df['class'].mean() * 100, 4),
        'total_fraud_amount': round(df.loc[df['class'] == 1, 'amount'].sum(), 2),
        'average_fraud_amount': round(df.loc[df['class'] == 1, 'amount'].mean(), 2)
    }
