import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_weather_data(start_year=2014, num_years=10, filepath='data/weather_data.csv'):
    np.random.seed(42)
    start_date = datetime(start_year, 1, 1)
    end_date = start_date + timedelta(days=365 * num_years - 1)
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    days = len(date_range)
    
    # 1. Base temperature: Seasonal pattern (sine wave) + global warming trend + noise
    # Let's say baseline avg temperature is 15°C
    day_of_year = date_range.dayofyear
    seasonal_variation = -12 * np.cos(2 * np.pi * day_of_year / 365) # Hotter in middle of year
    trend = np.linspace(0, 2, days) # Global warming trend over 10 years (2 degrees)
    noise = np.random.normal(0, 3, days)
    
    temperature = 15 + seasonal_variation + trend + noise
    
    # 2. Humidity: Higher in winter/rainy days
    base_humidity = 60 + 15 * np.cos(2 * np.pi * day_of_year / 365)
    humidity = base_humidity + np.random.normal(0, 5, days)
    humidity = np.clip(humidity, 20, 100) # clip between 20% and 100%
    
    # 3. Wind Speed: Random but slightly higher in spring/autumn
    wind_speed = np.random.gamma(shape=2, scale=3, size=days)
    wind_speed = np.clip(wind_speed, 0, 50)
    
    # 4. Pressure: Inverse to temperature broadly, normal around 1013 hPa
    pressure = 1013 - 0.5 * (temperature - 15) + np.random.normal(0, 5, days)
    
    # 5. Precipitation: Mostly 0, log-normal for rainy days, higher chance when humidity is high
    precip_chance = (humidity - 40) / 60
    precip_mask = np.random.uniform(0, 1, days) < precip_chance
    precipitation = np.where(precip_mask, np.random.exponential(scale=5, size=days), 0)
    
    # 6. Cloud Cover: 0 to 100, correlated with humidity and precipitation
    cloud_cover = humidity + np.where(precip_mask, 20, -10) + np.random.normal(0, 10, days)
    cloud_cover = np.clip(cloud_cover, 0, 100)
    
    df = pd.DataFrame({
        'date': date_range,
        'temperature': np.round(temperature, 1),
        'humidity': np.round(humidity, 1),
        'wind_speed': np.round(wind_speed, 1),
        'pressure': np.round(pressure, 1),
        'precipitation': np.round(precipitation, 1),
        'cloud_cover': np.round(cloud_cover, 1)
    })
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"[SUCCESS] Generated {days} days of weather data and saved to {filepath}")
    return df

if __name__ == "__main__":
    generate_weather_data()
