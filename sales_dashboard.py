# sales_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Data Simulation ---
@st.cache_data # Cache the data generation to speed up reruns
def generate_sales_data(start_date_str='2022-01-01', end_date_str='2023-12-31', seed=42):
    """Generates a realistic-looking sales dataset."""
    np.random.seed(seed)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    date_range = pd.date_range(start_date, end_date, freq='MS') # Monthly frequency

    regions = ['North', 'South', 'East', 'West']
    product_categories = ['Electronics', 'Apparel', 'Home Goods', 'Groceries']

    data = []
    for date in date_range:
        for region in regions:
            for category in product_categories:
                # Simulate base revenue with seasonality and trend
                month_of_year = date.month
                year_factor = 1 + (date.year - start_date.year) * 0.05 # Slight upward trend
                seasonality = 1 + np.sin((month_of_year - 1) * (2 * np.pi / 12)) * 0.1 # Simple seasonality
                base_revenue = np.random.uniform(5000, 15000) * seasonality * year_factor

                # Add some noise and region/category specific factors
                region_factor = {'North': 1.0, 'South': 0.9, 'East': 1.1, 'West': 0.95}[region]
                category_factor = {'Electronics': 1.2, 'Apparel': 0.8, 'Home Goods': 1.0, 'Groceries': 0.7}[category]
                revenue = base_revenue * region_factor * category_factor * np.random.uniform(0.9, 1.1)

                units_sold = int(revenue / np.random.uniform(50, 150)) # Price varies

                # Simulate Targets (e.g., 95% of simulated revenue + some variation)
                target_revenue = revenue * np.random.uniform(0.90, 1.05)

                # Simulate Previous Year Revenue (approx current revenue adjusted for trend)
                prev_year_revenue = revenue / (year_factor * np.random.uniform(0.98, 1.02)) if date.year > start_date.year else np.nan


                data.append({
                    'Date': date,
                    'Region': region,
                    'Product Category': category,
                    'Revenue': revenue,
                    'Units Sold': units_sold,
                    'Target Revenue': target_revenue,
                    'Previous Year Revenue': prev_year_revenue
                })

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['YearMonth'] = df['Date'].dt.to_period('M')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()

    # Add calculated fields
    df['Revenue vs Target (%)'] = ((df['Revenue'] / df['Target Revenue']) - 1) * 100
    df['YoY Growth (%)'] = ((df['Revenue'] / df['Previous Year Revenue']) - 1) * 100

    return df

# --- Streamlit App Layout ---

st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

# Load Data
df_orig = generate_sales_data()

st.title("📈 Regional Sales Performance Dashboard")
st.markdown("Analyze sales performance across regions, product categories, and time.")
st.markdown("---")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Time Period Filter
min_date = df_orig['Date'].min().date()
max_date = df_orig['Date'].max().date()
date_range_selection = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Filter data based on the transaction month."
)

# Convert selection back to datetime for filtering
start_date_filter = pd.to_datetime(date_range_selection[0])
end_date_filter = pd.to_datetime(date_range_selection[1])

# Region Filter
all_regions = df_orig['Region'].unique()
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=all_regions,
    default=all_regions,
    help="Choose specific regions to analyze. Default is all regions."
)

# Product Category Filter
all_categories = df_orig['Product Category'].unique()
selected_categories = st.sidebar.multiselect(
    "Select Product Categories",
    options=all_categories,
    default=all_categories,
    help="Choose specific product categories. Default is all categories."
)

# --- Filter Data based on Selections ---
df_filtered = df_orig[
    (df_orig['Date'] >= start_date_filter) &
    (df_orig['Date'] <= end_date_filter) &
    (df_orig['Region'].isin(selected_regions)) &
    (df_orig['Product Category'].isin(selected_categories))
].copy() # Use .copy() to avoid SettingWithCopyWarning

if df_filtered.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop() # Stop execution if no data

# --- Dashboard Content ---

# 1. Key Performance Indicators (KPIs) - Situational Awareness
st.header("Overall Performance Summary")

# Calculate KPIs
total_revenue = df_filtered['Revenue'].sum()
total_target = df_filtered['Target Revenue'].sum()
total_prev_year_revenue = df_filtered['Previous Year Revenue'].sum()
total_units_sold = df_filtered['Units Sold'].sum()

# Avoid division by zero
revenue_vs_target_perc = ((total_revenue / total_target) - 1) * 100 if total_target else 0
yoy_growth_perc = ((total_revenue / total_prev_year_revenue) - 1) * 100 if total_prev_year_revenue else 0

# Display KPIs using columns for layout
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta=f"{yoy_growth_perc:.1f}% vs PY",
        help="Total revenue for the selected period and filters. Delta shows Year-over-Year growth."
    )

with kpi_col2:
    st.metric(
        label="Revenue vs Target",
        value=f"{revenue_vs_target_perc:.1f}%",
        delta=f"Target: ${total_target:,.0f}",
        help="Percentage difference between actual revenue and target revenue. Delta shows the target value."
            # Use delta_color='inverse' or 'normal' based on whether positive is good/bad
            # delta_color = "normal" if revenue_vs_target_perc >= 0 else "inverse" # Requires manual calculation for color logic
    )
    # Note: Streamlit's delta color logic is simple (pos=green, neg=red).
    # For % vs Target, positive is good. For something like Costs vs Budget, positive might be bad.

with kpi_col3:
    st.metric(
        label="Total Units Sold",
        value=f"{total_units_sold:,}",
        help="Total number of units sold for the selected period and filters."
    )

st.markdown("---")

# 2. Performance by Dimension (Region & Product) - Exception Identification & Comparative Analysis
st.header("Performance Breakdown")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Region")
    # Aggregate data
    region_perf = df_filtered.groupby('Region')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    # Create chart
    fig_region = px.bar(
        region_perf,
        x='Region',
        y='Revenue',
        title="Total Revenue per Region",
        labels={'Revenue': 'Total Revenue ($)', 'Region': 'Sales Region'},
        color_discrete_sequence=px.colors.qualitative.Pastel, # Softer colors
        text_auto='.2s' # Format text labels on bars
    )
    fig_region.update_traces(textposition='outside')
    fig_region.update_layout(xaxis_title=None, yaxis_title="Total Revenue ($)") # Cleaner axes
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    st.subheader("Revenue by Product Category")
    # Aggregate data
    product_perf = df_filtered.groupby('Product Category')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False)
    # Create chart
    fig_product = px.bar(
        product_perf,
        x='Product Category',
        y='Revenue',
        title="Total Revenue per Product Category",
        labels={'Revenue': 'Total Revenue ($)', 'Product Category': 'Category'},
        color_discrete_sequence=px.colors.qualitative.Pastel1,
         text_auto='.2s'
    )
    fig_product.update_traces(textposition='outside')
    fig_product.update_layout(xaxis_title=None, yaxis_title="Total Revenue ($)")
    st.plotly_chart(fig_product, use_container_width=True)

st.markdown("---")

# 3. Trend Analysis - Pattern Recognition
st.header("Revenue Trend Over Time")

# Aggregate data by month
monthly_trend = df_filtered.groupby('YearMonth')[['Revenue', 'Target Revenue']].sum().reset_index()
monthly_trend['Date'] = monthly_trend['YearMonth'].dt.to_timestamp() # Convert Period to Timestamp for Plotly

fig_trend = go.Figure()

# Add Revenue Line
fig_trend.add_trace(go.Scatter(
    x=monthly_trend['Date'],
    y=monthly_trend['Revenue'],
    mode='lines+markers',
    name='Actual Revenue',
    line=dict(color='royalblue', width=2),
    marker=dict(size=5)
))

# Add Target Line
fig_trend.add_trace(go.Scatter(
    x=monthly_trend['Date'],
    y=monthly_trend['Target Revenue'],
    mode='lines',
    name='Target Revenue',
    line=dict(color='grey', width=2, dash='dash')
))

fig_trend.update_layout(
    title='Monthly Revenue vs Target',
    xaxis_title='Month',
    yaxis_title='Revenue ($)',
    hovermode='x unified', # Better hover experience
    legend_title_text='Metric'
)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# 4. Data Table - Progressive Disclosure
with st.expander("View Detailed Data (Filtered)"):
    st.dataframe(
        df_filtered[[
            'Date', 'Region', 'Product Category', 'Revenue',
            'Units Sold', 'Target Revenue', 'Revenue vs Target (%)',
            'Previous Year Revenue', 'YoY Growth (%)'
        ]].sort_values(by="Date", ascending=False).style.format({ # Apply formatting for readability
            "Revenue": "${:,.2f}",
            "Target Revenue": "${:,.2f}",
            "Previous Year Revenue": "${:,.2f}",
            "Revenue vs Target (%)": "{:.1f}%",
            "YoY Growth (%)": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True # Cleaner look
    )

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Dashboard developed for INDIVIDUAL ACTIVITY 3. Uses simulated data.")