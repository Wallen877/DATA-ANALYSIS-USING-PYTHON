import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Color scheme
COLORS = {'Churned': '#d62728', 'Retained': '#2ca02c', 'Neutral': '#1f77b4'}

# Load the data
print("Loading data...")
df = pd.read_csv('Ecom Data.csv')

print(f"\nDataset shape: {df.shape}")
print(f"\nColumn names and types:")
print(df.dtypes)

# ==================== DATA CLEANING ====================
print("\n" + "="*50)
print("DATA CLEANING")
print("="*50)

# Show missing values before cleaning
print("\nMissing values before cleaning:")
missing_before = df.isnull().sum()
print(missing_before[missing_before > 0])

# 1. Handle missing values
# For numeric columns, fill with median
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)

# 2. Handle missing values in categorical columns
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].mode()[0], inplace=True)

# 3. Remove duplicates
initial_rows = len(df)
df.drop_duplicates(inplace=True)
print(f"\nRemoved {initial_rows - len(df)} duplicate rows")

# 4. Data type conversions
df['Churned'] = df['Churned'].astype(int)
df['Signup_Quarter'] = df['Signup_Quarter'].astype(str)

# 5. Outlier detection and handling (using IQR method)
print("\nDetecting and handling outliers...")
outlier_cols = ['Age', 'Login_Frequency', 'Session_Duration_Avg', 'Total_Purchases', 'Average_Order_Value']
for col in outlier_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Cap outliers instead of removing
    df[col] = df[col].clip(lower_bound, upper_bound)

print("\nMissing values after cleaning:")
print(f"Total missing values: {df.isnull().sum().sum()}")

print(f"\nCleaned dataset shape: {df.shape}")
print("\nData Cleaning Complete!")

# ==================== DATA SUMMARY ====================
print("\n" + "="*50)
print("DATA SUMMARY")
print("="*50)
print(df.describe())

# Save cleaned data
cleaned_filename = 'Ecom_Data_Cleaned.csv'
df.to_csv(cleaned_filename, index=False)
print(f"\nCleaned data saved to {cleaned_filename}")

# ==================== CREATE INTERACTIVE DASHBOARD ====================
print("\n" + "="*50)
print("CREATING INTERACTIVE DASHBOARD")
print("="*50)

# Create subplots with multiple visualizations
fig = make_subplots(
    rows=4, cols=2,
    subplot_titles=(
        'Customer Age Distribution',
        'Churn Rate by Country',
        'Total Purchases vs Average Order Value',
        'Customer Lifetime Value Distribution',
        'Login Frequency Distribution',
        'Cart Abandonment Rate',
        'Membership Years Distribution',
        'Top Countries by Customer Count'
    ),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# 1. Age Distribution
fig.add_trace(
    go.Histogram(x=df['Age'], name='Age', nbinsx=30, marker_color=COLORS['Neutral']),
    row=1, col=1
)

# 2. Churn Rate by Country
churn_by_country = df.groupby('Country')['Churned'].agg(['sum', 'count'])
churn_by_country['rate'] = (churn_by_country['sum'] / churn_by_country['count'] * 100).sort_values(ascending=False).head(10)
fig.add_trace(
    go.Bar(x=churn_by_country['rate'].index, y=churn_by_country['rate'].values, 
           name='Churn Rate %', marker_color=COLORS['Churned']),
    row=1, col=2
)

# 3. Total Purchases vs Average Order Value
fig.add_trace(
    go.Scatter(x=df['Total_Purchases'], y=df['Average_Order_Value'],
               mode='markers', name='Purchases vs Order Value',
               marker=dict(color=df['Churned'], colorscale='RdYlGn_r', size=4),
               text=df['Country'], hovertemplate='<b>Purchases:</b> %{x}<br><b>Avg Order Value:</b> $%{y:.2f}<extra></extra>'),
    row=2, col=1
)

# 4. Lifetime Value Distribution
fig.add_trace(
    go.Histogram(x=df['Lifetime_Value'], name='Lifetime Value', nbinsx=40, marker_color=COLORS['Retained']),
    row=2, col=2
)

# 5. Login Frequency Distribution
fig.add_trace(
    go.Box(y=df['Login_Frequency'], name='Login Frequency', marker_color=COLORS['Churned']),
    row=3, col=1
)

# 6. Cart Abandonment Rate
fig.add_trace(
    go.Histogram(x=df['Cart_Abandonment_Rate'], name='Cart Abandonment %', nbinsx=30, marker_color=COLORS['Neutral']),
    row=3, col=2
)

# 7. Churn Distribution
fig.add_trace(
    go.Histogram(x=df['Membership_Years'], name='Membership Years', nbinsx=30, marker_color=COLORS['Neutral']),
    row=4, col=1
)

# 8. Top Countries
top_countries = df['Country'].value_counts().head(10)
fig.add_trace(
    go.Bar(x=top_countries.values, y=top_countries.index, orientation='h',
           name='Customer Count', marker_color=COLORS['Retained']),
    row=4, col=2
)

# Update layout
fig.update_layout(
    title_text='<b>Ecommerce Customer Analytics Dashboard</b>',
    height=1400,
    showlegend=False,
    template='plotly_white'
)

# Update y-axes labels
fig.update_yaxes(title_text="Frequency", row=1, col=1)
fig.update_yaxes(title_text="Churn Rate %", row=1, col=2)
fig.update_yaxes(title_text="Avg Order Value ($)", row=2, col=1)
fig.update_yaxes(title_text="Frequency", row=2, col=2)
fig.update_yaxes(title_text="Login Frequency", row=3, col=1)
fig.update_yaxes(title_text="Frequency", row=3, col=2)
fig.update_yaxes(title_text="Frequency", row=4, col=1)
fig.update_yaxes(title_text="Country", row=4, col=2)

# Update x-axes labels
fig.update_xaxes(title_text="Age", row=1, col=1)
fig.update_xaxes(title_text="Country", row=1, col=2)
fig.update_xaxes(title_text="Total Purchases", row=2, col=1)
fig.update_xaxes(title_text="Lifetime Value ($)", row=2, col=2)
fig.update_xaxes(title_text="Login Frequency", row=3, col=1)
fig.update_xaxes(title_text="Cart Abandonment Rate %", row=3, col=2)
fig.update_xaxes(title_text="Membership Years", row=4, col=1)
fig.update_xaxes(title_text="Customer Count", row=4, col=2)

# Save main dashboard
dashboard_file = 'dashboard_overview.html'
fig.write_html(dashboard_file)
print(f"Main dashboard saved to {dashboard_file}")

# ==================== ADDITIONAL DETAILED DASHBOARDS ====================

# 1. Churn Analysis Dashboard
fig_churn = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Churn by Login Frequency', 'Churn by Cart Abandonment Rate',
                    'Churn by Customer Service Calls', 'Days Since Last Purchase - Churned vs Retained')
)

for churned_status, name in [(0, 'Retained'), (1, 'Churned')]:
    subset = df[df['Churned'] == churned_status]
    fig_churn.add_trace(
        go.Histogram(x=subset['Login_Frequency'], name=name, opacity=0.7),
        row=1, col=1
    )

for churned_status, name in [(0, 'Retained'), (1, 'Churned')]:
    subset = df[df['Churned'] == churned_status]
    fig_churn.add_trace(
        go.Histogram(x=subset['Cart_Abandonment_Rate'], name=name, opacity=0.7, showlegend=False),
        row=1, col=2
    )

fig_churn.add_trace(
    go.Box(y=df[df['Churned']==0]['Customer_Service_Calls'], name='Retained', marker_color=COLORS['Retained']),
    row=2, col=1
)
fig_churn.add_trace(
    go.Box(y=df[df['Churned']==1]['Customer_Service_Calls'], name='Churned', marker_color=COLORS['Churned']),
    row=2, col=1
)

fig_churn.add_trace(
    go.Box(y=df[df['Churned']==0]['Days_Since_Last_Purchase'], name='Retained', marker_color=COLORS['Retained'], showlegend=False),
    row=2, col=2
)
fig_churn.add_trace(
    go.Box(y=df[df['Churned']==1]['Days_Since_Last_Purchase'], name='Churned', marker_color=COLORS['Churned'], showlegend=False),
    row=2, col=2
)

fig_churn.update_layout(title_text='<b>Churn Analysis Dashboard</b>', height=800, template='plotly_white')
fig_churn.update_yaxes(title_text="Count", row=1, col=1)
fig_churn.update_yaxes(title_text="Count", row=1, col=2)
fig_churn.update_yaxes(title_text="Service Calls", row=2, col=1)
fig_churn.update_yaxes(title_text="Days Since Purchase", row=2, col=2)
churn_file = 'dashboard_churn_analysis.html'
fig_churn.write_html(churn_file)
print(f"Churn analysis dashboard saved to {churn_file}")

# 2. Geographic Dashboard
geographic_data = df.groupby('Country').agg({
    'Churned': 'mean',
    'Lifetime_Value': 'mean',
    'Total_Purchases': 'mean',
    'Age': 'mean'
}).reset_index()

fig_geo = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Average Lifetime Value by Country', 'Average Purchases by Country',
                    'Churn Rate by Country', 'Average Customer Age by Country')
)

fig_geo.add_trace(
    go.Bar(x=geographic_data['Country'], y=geographic_data['Lifetime_Value'],
           name='Avg Lifetime Value', marker_color=COLORS['Neutral']),
    row=1, col=1
)

fig_geo.add_trace(
    go.Bar(x=geographic_data['Country'], y=geographic_data['Total_Purchases'],
           name='Avg Purchases', marker_color=COLORS['Retained']),
    row=1, col=2
)

fig_geo.add_trace(
    go.Bar(x=geographic_data['Country'], y=geographic_data['Churned']*100,
           name='Churn Rate %', marker_color=COLORS['Churned']),
    row=2, col=1
)

fig_geo.add_trace(
    go.Bar(x=geographic_data['Country'], y=geographic_data['Age'],
           name='Avg Age', marker_color=COLORS['Retained']),
    row=2, col=2
)

fig_geo.update_layout(title_text='<b>Geographic Analysis Dashboard</b>', height=800, template='plotly_white', showlegend=False)
fig_geo.update_yaxes(title_text="Value ($)", row=1, col=1)
fig_geo.update_yaxes(title_text="Purchases", row=1, col=2)
fig_geo.update_yaxes(title_text="Churn Rate %", row=2, col=1)
fig_geo.update_yaxes(title_text="Age", row=2, col=2)
geo_file = 'dashboard_geographic.html'
fig_geo.write_html(geo_file)
print(f"Geographic dashboard saved to {geo_file}")

# 3. Choropleth Map - Churn Rate by Country
country_mapping = {
    'USA': 'United States',
    'UK': 'United Kingdom',
    'Germany': 'Germany',
    'France': 'France',
    'Japan': 'Japan',
    'India': 'India',
    'Canada': 'Canada',
    'Australia': 'Australia'
}

choro_data = geographic_data.copy()
choro_data['Country_Full'] = choro_data['Country'].map(country_mapping)

fig_choropleth = go.Figure(data=go.Choropleth(
    locations=choro_data['Country_Full'],
    z=choro_data['Churned']*100,
    locationmode='country names',
    colorscale='Reds',
    text=choro_data['Country'],
    hovertemplate='<b>%{text}</b><br>Churn Rate: %{z:.2f}%<extra></extra>',
    colorbar=dict(title="Churn Rate %"),
    marker_line_color='rgba(0,0,0,0.2)',
    marker_line_width=1
))

fig_choropleth.update_layout(
    title_text='<b>Global Churn Rate by Country</b>',
    geo=dict(
        projection_type='natural earth',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)'
    ),
    height=600,
    template='plotly_white'
)

choro_file = 'dashboard_choropleth_map.html'
fig_choropleth.write_html(choro_file)
print(f"Choropleth map saved to {choro_file}")

# ==================== KEY METRICS & INSIGHTS ====================
print("\n" + "="*50)
print("KEY METRICS & INSIGHTS")
print("="*50)

overall_churn_rate = (df['Churned'].sum() / len(df)) * 100
avg_lifetime_value = df['Lifetime_Value'].mean()
avg_purchases = df['Total_Purchases'].mean()
avg_age = df['Age'].mean()

print(f"\n📊 OVERALL METRICS:")
print(f"  • Total Customers: {len(df):,}")
print(f"  • Churn Rate: {overall_churn_rate:.2f}%")
print(f"  • Average Lifetime Value: ${avg_lifetime_value:.2f}")
print(f"  • Average Purchases per Customer: {avg_purchases:.2f}")
print(f"  • Average Customer Age: {avg_age:.2f} years")

print(f"\n🌍 GEOGRAPHIC INSIGHTS:")
top_country = df['Country'].value_counts().index[0]
print(f"  • Most Customers From: {top_country} ({df[df['Country']==top_country].shape[0]:,} customers)")

highest_churn = geographic_data.loc[geographic_data['Churned'].idxmax()]
print(f"  • Highest Churn Rate: {highest_churn['Country']} ({highest_churn['Churned']*100:.2f}%)")

highest_ltv = geographic_data.loc[geographic_data['Lifetime_Value'].idxmax()]
print(f"  • Highest Avg Lifetime Value: {highest_ltv['Country']} (${highest_ltv['Lifetime_Value']:.2f})")

print(f"\n👥 CUSTOMER SEGMENTS:")
high_value = df[df['Lifetime_Value'] > df['Lifetime_Value'].quantile(0.75)]
print(f"  • High-Value Customers (Top 25%): {len(high_value):,} (Avg LTV: ${high_value['Lifetime_Value'].mean():.2f})")

low_value = df[df['Lifetime_Value'] < df['Lifetime_Value'].quantile(0.25)]
print(f"  • Low-Value Customers (Bottom 25%): {len(low_value):,} (Avg LTV: ${low_value['Lifetime_Value'].mean():.2f})")

churned_customers = df[df['Churned'] == 1]
print(f"  • Churned Customers: {len(churned_customers):,} (Churn Rate: {(len(churned_customers)/len(df))*100:.2f}%)")

print("\n✅ DASHBOARD CREATION COMPLETE!")
print(f"\n📁 Generated files:")
print(f"  • {cleaned_filename}")
print(f"  • {dashboard_file}")
print(f"  • {churn_file}")
print(f"  • {geo_file}")
print(f"  • {choro_file}")
print("\n🎨 Open the .html files in your browser to view the interactive dashboards!")
