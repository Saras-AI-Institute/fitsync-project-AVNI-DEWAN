import pandas as pd


def load_data(filepath='data/health_data.csv'):
    """
    Load health data from CSV, clean missing values, and standardize column names.
    """
    df = pd.read_csv(filepath)

    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    # Rename possible column variations
    df.rename(columns={
        'Sleep_Hours': 'Sleep_hours',
        'sleep_hours': 'Sleep_hours',
        'Heart_Rate_bpm': 'heart_rate_bpm',
        'Heart_rate_bpm': 'heart_rate_bpm'
    }, inplace=True)

    if 'Steps' in df.columns:
        df['Steps'].fillna(df['Steps'].median(), inplace=True)

    if 'Sleep_hours' in df.columns:
        df['Sleep_hours'].fillna(7.0, inplace=True)

    if 'heart_rate_bpm' in df.columns:
        df['heart_rate_bpm'].fillna(68, inplace=True)

    for column in df.columns:
        if df[column].isnull().any() and df[column].dtype != 'object':
            df[column].fillna(df[column].median(), inplace=True)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    return df


def calculate_recovery_score(df):
    """
    Calculate Recovery Score
    """
    df['Recovery_Score'] = 50

    if 'Sleep_hours' in df.columns:
        df.loc[df['Sleep_hours'] >= 7, 'Recovery_Score'] += 20
        df.loc[df['Sleep_hours'] < 6, 'Recovery_Score'] -= 15

    if 'heart_rate_bpm' in df.columns:
        df.loc[df['heart_rate_bpm'] <= 70, 'Recovery_Score'] += 10
        df.loc[df['heart_rate_bpm'] > 85, 'Recovery_Score'] -= 10

    if 'Steps' in df.columns:
        df.loc[df['Steps'] >= 8000, 'Recovery_Score'] += 5
        df.loc[df['Steps'] < 4000, 'Recovery_Score'] -= 5
        df.loc[df['Steps'] > 14000, 'Recovery_Score'] -= 5

    df['Recovery_Score'] = df['Recovery_Score'].clip(0, 100)

    return df


def process_data():
    df = load_data()
    df = calculate_recovery_score(df)
    return df