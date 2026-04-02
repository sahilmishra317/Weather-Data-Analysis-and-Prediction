# Weather Data Analysis and Prediction

A comprehensive internship project focusing on time-series analysis and predicting future temperature trends using regression models.

## Structure
- `data/`: Contains the generated synthetic weather dataset.
- `analysis/`: Python scripts for EDA, feature engineering, and modeling.
- `output/`: Generated output charts, metrics, and JSON data.
- `dashboard/`: Interactive web dashboard for visualizing the results.

## Quick Start
1. Install requirements: `pip install -r requirements.txt`
2. Run data pipeline: `python analysis/run_all.py`
3. Serve dashboard locally, for example: `python -m http.server 8000 --directory dashboard` and open `http://localhost:8000/` in browser.

## Technologies Used
- **Data Science**: Python, Pandas, Numpy, Scikit-learn, Matplotlib, Seaborn
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript, Chart.js
