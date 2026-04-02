import pandas as pd
import numpy as np
import json
import joblib
from datetime import timedelta

def forecast_future(input_file='data/weather_features.csv', model_file='output/random_forest.pkl', output_file='output/predictions.json'):
    print("Starting Forecasting...")
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    
    # Load best model (Random Forest)
    rf = joblib.load(model_file)
    
    # Simulate features for the next 365 days
    last_date = df['date'].iloc[-1]
    
    future_dates = [last_date + timedelta(days=i) for i in range(1, 366)]
    
    # We will use simple heuristics to generate future features to feed into the model
    # Better approach would be iterative forecasting, but this is a simplified demo
    
    predictions = []
    
    for i, date in enumerate(future_dates):
        day_of_year = date.dayofyear
        year = date.year
        day_sin = np.sin(2 * np.pi * day_of_year / 365)
        day_cos = np.cos(2 * np.pi * day_of_year / 365)
        
        # Average historical rolling means to use as dummy input
        temp_roll_7 = df[df['date'].dt.dayofyear == day_of_year]['temperature'].mean()
        temp_roll_30 = temp_roll_7 # simplify
        humidity = df[df['date'].dt.dayofyear == day_of_year]['humidity'].mean()
        pressure = df[df['date'].dt.dayofyear == day_of_year]['pressure'].mean()
        
        # In case it's Feb 29 and we don't have historical
        if np.isnan(temp_roll_7):
            temp_roll_7 = 15
            temp_roll_30 = 15
            humidity = 60
            pressure = 1013
            
        features = pd.DataFrame([{
            'day_sin': day_sin,
            'day_cos': day_cos,
            'year': year,
            'temp_roll_7': temp_roll_7,
            'temp_roll_30': temp_roll_30,
            'humidity': humidity,
            'pressure': pressure
        }])
        
        pred_temp = rf.predict(features)[0]
        
        predictions.append({
            'date': date.strftime('%Y-%m-%d'),
            'predicted_temp': round(pred_temp, 2)
        })
        
    with open(output_file, 'w') as f:
        json.dump(predictions, f, indent=4)
        
    print(f"[SUCCESS] Forecasting completed. Saved to {output_file}")

if __name__ == "__main__":
    forecast_future()
