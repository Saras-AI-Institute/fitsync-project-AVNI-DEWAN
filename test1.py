from modules.processor import load_data, calculate_recovery_score

df = load_data()
df = calculate_recovery_score(df)

df.loc[df['Sleep_hours'] >= 7, 'Recovery_Score'] += 20

print(df[['Date', 'Sleep_hours', 'heart_rate_bpm', 'Recovery_Score']].head(10))