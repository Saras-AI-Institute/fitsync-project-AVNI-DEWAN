def load_data():
    """
    Load health data from a CSV file, handle missing values, and convert the date column.

    Returns:
        pd.DataFrame: Cleaned pandas DataFrame.
    """
    # Read the CSV file
    df = pd.read_csv('data/health_data.csv')
    
    # Fill missing 'Steps' with its median
    if 'Steps' in df.columns:
        df['Steps'].fillna(df['Steps'].median(), inplace=True)
    
    # Fill missing 'Sleep_hours' with 7.0
    if 'Sleep_hours' in df.columns:
        df['Sleep_hours'].fillna(7.0, inplace=True)
    
    # Fill missing 'heart_rate_bpm' with 68
    if 'heart_rate_bpm' in df.columns:
        df['heart_rate_bpm'].fillna(68, inplace=True)
    
    # For other numeric columns, fill missing values with their median
    numeric_columns = df.select_dtypes(include='number').columns.difference(['Steps', 'Sleep_hours', 'heart_rate_bpm'])
    for column in numeric_columns:
        df[column].fillna(df[column].median(), inplace=True)
    
    # Convert 'date' column to datetime objects
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Return the cleaned DataFrame
    return df


def calculate_recovery_score(df):
    """
    Calculate and add a 'Recovery_Score' column to the DataFrame based on sleep hours, heart rate, and steps.

    Parameters:
        df (pd.DataFrame): DataFrame containing health metrics.

    Returns:
        pd.DataFrame: DataFrame with a new 'Recovery_Score' column.
    """
    # Initialize the Recovery_Score column with a base score of 50
    df['Recovery_Score'] = 50

    # Adjust the score based on Sleep Hours
    # Good sleep (7+ hours) improves the recovery score significantly
    df.loc[df['Sleep_hours'] >= 7, 'Recovery_Score'] += 20
    # Poor sleep (less than 6 hours) heavily reduces the recovery score
    df.loc[df['Sleep_hours'] < 6, 'Recovery_Score'] -= 15

    # Adjust the score based on Heart Rate bpm
    # Lower heart rates are better for recovery
    df.loc[df['heart_rate_bpm'] <= 70, 'Recovery_Score'] += 10
    # Higher heart rates might indicate stress or poor recovery
    df.loc[df['heart_rate_bpm'] > 85, 'Recovery_Score'] -= 10

    # Adjust the score based on Steps
    # Moderate activity (steps between 8000 and 14000) is good
    df.loc[df['Steps'] >= 8000, 'Recovery_Score'] += 5
    # Very low or very high activity might reduce recovery
    df.loc[df['Steps'] < 4000, 'Recovery_Score'] -= 5
    df.loc[df['Steps'] > 14000, 'Recovery_Score'] -= 5

    # Ensure the Recovery_Score stays within the range [0, 100]
    df['Recovery_Score'] = df['Recovery_Score'].clip(lower=0, upper=100)

    return df