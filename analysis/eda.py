import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

def run_eda(input_file='data/weather_data.csv', output_dir='output'):
    print("Starting Exploratory Data Analysis...")
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Temperature Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['temperature'], kde=True, bins=50, color='coral')
    plt.title('Distribution of Daily Temperatures')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.savefig(f'{output_dir}/temperature_distribution.png')
    plt.close()
    
    # 2. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    corr = df.drop('date', axis=1).corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Match Matrix of Weather Variables')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/correlation_heatmap.png')
    plt.close()

    # 3. Monthly Averages (JSON for Dashboard)
    df['month'] = df['date'].dt.month
    monthly_avg = df.groupby('month')['temperature'].mean().round(2).to_dict()
    
    with open(f'{output_dir}/monthly_averages.json', 'w') as f:
        json.dump(monthly_avg, f, indent=4)
        
    print(f"[SUCCESS] EDA completed. Outputs saved to {output_dir}")

if __name__ == "__main__":
    run_eda()
