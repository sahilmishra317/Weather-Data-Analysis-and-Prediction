import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import joblib

def evaluate_model(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 3)
    }

def train_models(input_file='data/weather_features.csv', output_dir='output'):
    print("Starting Model Training...")
    df = pd.read_csv(input_file)
    
    # Features (X) and Target (y)
    # We will predict next day's temperature (we shift temp backwards)
    df['target_temp'] = df['temperature'].shift(-1)
    df = df.dropna()
    
    features = ['day_sin', 'day_cos', 'year', 'temp_roll_7', 'temp_roll_30', 'humidity', 'pressure']
    X = df[features]
    y = df['target_temp']
    
    # Train/Test Split (80/20) - Chronological split
    train_size = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]
    
    models = {}
    metrics = {}
    
    # 1. Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    metrics['Linear Regression'] = evaluate_model(y_test, lr_pred, 'Linear Regression')
    joblib.dump(lr, f'{output_dir}/linear_model.pkl')
    
    # 2. Polynomial Regression (Degree 2)
    poly = PolynomialFeatures(degree=2)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    pr = LinearRegression()
    pr.fit(X_train_poly, y_train)
    pr_pred = pr.predict(X_test_poly)
    metrics['Polynomial Regression'] = evaluate_model(y_test, pr_pred, 'Polynomial Regression')
    
    # 3. Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    metrics['Random Forest'] = evaluate_model(y_test, rf_pred, 'Random Forest')
    joblib.dump(rf, f'{output_dir}/random_forest.pkl')
    
    # Save Metrics to JSON
    with open(f'{output_dir}/model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print(f"[SUCCESS] Modeling completed. Metrics saved to {output_dir}/model_metrics.json")
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    train_models()
