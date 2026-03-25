import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate date range
start_date = "2025-01-01"
dates = pd.date_range(start=start_date, periods=365)

# Generate realistic fitness data
steps = np.random.normal(loc=8500, scale=2500, size=len(dates)).clip(3000, 18000)
sleep_hours = np.random.normal(loc=7.2, scale=1.0, size=len(dates)).clip(4.5, 9.5)
heart_rate_bpm = np.random.normal(loc=68, scale=10, size=len(dates)).clip(48, 110)
calories_burned = np.random.randint(1800, 4200, size=len(dates))
active_minutes = np.random.randint(20, 180, size=len(dates))

# Create DataFrame
fitness_data = pd.DataFrame({
    'Date': dates,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate_bpm,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Introduce 5% missing values per column
for column in fitness_data.columns[1:]:  # Skip 'Date' column
    fitness_data.loc[fitness_data.sample(frac=0.05).index, column] = np.nan

# Save to CSV in the data folder
fitness_data.to_csv('data/health_data.csv', index=False)

print('Generated data saved to data/health_data.csv')