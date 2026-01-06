# E-Commerce Dashboard Project

An interactive data analysis and visualization project for e-commerce customer analytics using Python, Pandas, and Plotly.

## Overview

This project performs comprehensive data cleaning and analysis on a 50,000+ customer e-commerce dataset, generating four interactive dashboards for business intelligence.

## Features

- **Data Cleaning**: Handles missing values, detects outliers, removes duplicates
- **Interactive Dashboards**: Multiple visualization dashboards using Plotly
- **Geographic Analysis**: Country-level churn and performance metrics
- **Churn Analysis**: Deep dive into customer churn patterns and indicators
- **Choropleth Map**: Global visualization of churn rates by country

## Dashboards Generated

1. **dashboard_overview.html** - Comprehensive overview with 8 key metrics
   - Customer age distribution
   - Churn rates by country
   - Purchase vs order value analysis
   - Lifetime value distribution
   - And more...

2. **dashboard_churn_analysis.html** - Churn-focused analysis
   - Login frequency impact on churn
   - Cart abandonment patterns
   - Customer service interactions
   - Days since last purchase

3. **dashboard_geographic.html** - Geographic performance metrics
   - Average lifetime value by country
   - Purchase patterns by country
   - Churn rates by country
   - Average customer age by region

4. **dashboard_choropleth_map.html** - Interactive world map
   - Global churn rate visualization
   - Color-coded by churn intensity

## Key Insights

- **Total Customers**: 50,000
- **Overall Churn Rate**: 28.90%
- **Average Lifetime Value**: $1,440.63
- **Average Purchases**: 12.98 per customer
- **High-Value Customers**: 12,500 (Avg LTV: $2,691.01)

## Requirements

- Python 3.x
- pandas
- numpy
- plotly
- kaleido

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ecommerce-dashboard.git
cd ecommerce-dashboard

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pandas numpy plotly kaleido
```

## Usage

```bash
# Run the dashboard generation script
python ecommerce_dashboard.py
```

This will:
1. Load and clean the data (Ecom Data.csv)
2. Generate cleaned dataset (Ecom_Data_Cleaned.csv)
3. Create four interactive HTML dashboards

## Color Scheme

- 🔴 **Churned**: #d62728 (Red) - Customer churn indicators
- 🟢 **Retained**: #2ca02c (Green) - Healthy customer metrics
- 🔵 **Neutral**: #1f77b4 (Blue) - General analytics

## File Structure

```
ecommerce-dashboard/
├── ecommerce_dashboard.py          # Main script
├── Ecom Data.csv                   # Raw dataset
├── Ecom_Data_Cleaned.csv           # Cleaned dataset
├── dashboard_overview.html         # Main dashboard
├── dashboard_churn_analysis.html   # Churn analysis
├── dashboard_geographic.html       # Geographic metrics
├── dashboard_choropleth_map.html   # World map visualization
├── .gitignore
└── README.md
```

## Data Processing

### Cleaning Steps:
1. Fill missing numeric values with median
2. Fill missing categorical values with mode
3. Remove duplicate records
4. Convert data types appropriately
5. Cap outliers using IQR method (1.5 * IQR)

### Dataset Features (25 columns):
- Customer demographics (Age, Gender, Country, City)
- Engagement metrics (Login Frequency, Session Duration)
- Purchase behavior (Total Purchases, Average Order Value)
- Churn indicator and signup quarter

## Author

Created as part of e-commerce analytics project

## License

MIT License
