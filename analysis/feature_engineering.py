import pandas as pd
import numpy as np
import os

def engineer_features(input_file='data/weather_data.csv', output_file='data/weather_features.csv'):
    print("Starting Feature Engineering...")
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    
    # Time-based features
    df['day_of_year'] = df['date'].dt.dayofyear
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    # Cyclical encoding for day of year
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
    # Rolling averages (past 7 days, 30 days)
    # Ensure sorted by date
    df = df.sort_values('date')
    df['temp_roll_7'] = df['temperature'].rolling(window=7, min_periods=1).mean()
    df['temp_roll_30'] = df['temperature'].rolling(window=30, min_periods=1).mean()
    
    # Lag features (previous day's temp)
    df['temp_lag_1'] = df['temperature'].shift(1)
    df['temp_lag_7'] = df['temperature'].shift(7)
    
    # Drop NAs created by lags
    df = df.bfill()
    
    df.to_csv(output_file, index=False)
    print(f"[SUCCESS] Feature engineering completed. Output saved to {output_file}")
    return df

if __name__ == "__main__":
    engineer_features()
