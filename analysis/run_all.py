from eda import run_eda
from feature_engineering import engineer_features
from models import train_models
from predict import forecast_future
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data'))
from generate_weather_data import generate_weather_data

def main():
    print("=== WEATHER DATA ANALYSIS PIPELINE ===")
    
    # 1. Generate Data
    print("\n--- Phase 1: Data Generation ---")
    generate_weather_data()
    
    # 2. Extract Features
    print("\n--- Phase 2: Feature Engineering ---")
    engineer_features()
    
    # 3. Exploratory Data Analysis
    print("\n--- Phase 3: Exploratory Data Analysis ---")
    run_eda()
    
    # 4. Train Models
    print("\n--- Phase 4: Model Training ---")
    train_models()
    
    # 5. Forecast Future
    print("\n--- Phase 5: Predictive Forecasting ---")
    forecast_future()
    
    print("\n=== PIPELINE SUCCESSFUL ===")
    print("Dashboard data is ready in the 'output' folder!")

if __name__ == "__main__":
    main()
