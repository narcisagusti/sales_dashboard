# sales_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Enhanced Data Simulation ---
@st.cache_data # Cache the data generation
def generate_enhanced_sales_data(start_date_str='2022-01-01', end_date_str='2023-12-31', seed=42):
    np.random.seed(seed)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    date_range = pd.date_range(start_date, end_date, freq='D') # Daily for more granularity if needed, then aggregate

    regions = ['North', 'South', 'East', 'West', 'Central']
    product_categories_subs = {
        'Electronics': ['Smartphones', 'Laptops', 'Accessories'],
        'Apparel': ['Men\'s Clothing', 'Women\'s Clothing', 'Footwear'],
        'Home Goods': ['Furniture', 'Kitchenware', 'Decor'],
        'Groceries': ['Fresh Produce', 'Pantry Staples', 'Beverages']
    }
    salespersons = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry']

    data = []
    for date_val in date_range:
        # Simulate fewer transactions per day for realism
        num_transactions_today = np.random.randint(5, 25)
        for _ in range(num_transactions_today):
            region = np.random.choice(regions)
            category = np.random.choice(list(product_categories_subs.keys()))
            sub_category = np.random.choice(product_categories_subs[category])
            salesperson = np.random.choice(salespersons)

            # Simulate base revenue with seasonality and trend
            month_of_year = date_val.month
            year_factor = 1 + (date_val.year - start_date.year) * 0.08 # Slightly stronger trend
            seasonality = 1 + np.sin((month_of_year - 1) * (2 * np.pi / 12)) * 0.15
            base_revenue_per_transaction = np.random.uniform(20, 300) * seasonality * year_factor

            # Add factors
            region_factor = {'North': 1.0, 'South': 0.9, 'East': 1.1, 'West': 0.95, 'Central': 1.05}[region]
            cat_factor = {'Electronics': 1.3, 'Apparel': 0.8, 'Home Goods': 1.0, 'Groceries': 0.7}[category]
            sub_cat_factor = np.random.uniform(0.8, 1.2) # Sub-category variance

            revenue = base_revenue_per_transaction * region_factor * cat_factor * sub_cat_factor * np.random.uniform(0.9, 1.1)
            units_sold = max(1, int(revenue / np.random.uniform(10, 100))) # Price varies

            target_revenue = revenue * np.random.uniform(0.85, 1.10)
            cogs_percentage = np.random.uniform(0.4, 0.7) # Cost is 40-70% of revenue
            cogs = revenue * cogs_percentage
            profit = revenue - cogs

            prev_year_date = date_val - pd.DateOffset(years=1)
            # Simulate prev_year_revenue: look up similar month in df later or estimate
            # For simplicity in generation, we'll estimate it here
            prev_year_revenue = revenue / (year_factor * np.random.uniform(0.95, 1.05)) if date_val.year > start_date.year else np.nan

            data.append({
                'Date': date_val,
                'Region': region,
                'Product Category': category,
                'Sub-Category': sub_category,
                'Salesperson': salesperson,
                'Revenue': revenue,
                'Units Sold': units_sold,
                'Target Revenue': target_revenue,
                'COGS': cogs,
                'Profit': profit,
                'Previous Year Revenue': prev_year_revenue
            })

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.to_period('Q').astype(str) # Q1, Q2 etc. as string
    df['Month'] = df['Date'].dt.month_name()
    df['YearMonth'] = df['Date'].dt.to_period('M')

    df['Revenue vs Target (%)'] = ((df['Revenue'] / df['Target Revenue']) - 1) * 100
    df['YoY Revenue Growth (%)'] = ((df['Revenue'] / df['Previous Year Revenue']) - 1) * 100
    df['Profit Margin (%)'] = (df['Profit'] / df['Revenue']) * 100
    df.replace([np.inf, -np.inf], np.nan, inplace=True) # Handle potential division by zero

    return df

# --- Helper Functions for Plotting ---
def create_bar_chart(df, x_col, y_col, title, color_col=None, y_label=None, x_label=None, color_sequence=px.colors.qualitative.Plotly):
    if y_label is None: y_label = y_col
    if x_label is None: x_label = x_col
    fig = px.bar(df, x=x_col, y=y_col, title=title, labels={y_col: y_label, x_col: x_label},
                 color=color_col, text_auto='.2s', color_discrete_sequence=color_sequence)
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    return fig

def create_line_chart(df, x_col, y_cols, title, y_labels=None, x_label=None, legend_title=None):
    if x_label is None: x_label = x_col
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly
    for i, y_col in enumerate(y_cols):
        y_lab = y_labels[i] if y_labels and i < len(y_labels) else y_col
        fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines+markers', name=y_lab,
                                 line=dict(color=colors[i % len(colors)])))
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title="Value", hovermode="x unified", legend_title_text=legend_title)
    return fig

def create_treemap(df, path_cols, values_col, title, color_col=None):
    fig = px.treemap(df, path=path_cols, values=values_col, title=title,
                     color=color_col, color_continuous_scale='RdBu',
                     hover_data={values_col:':.2f'})
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig

# --- Streamlit App Layout ---
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Load Data
df_orig = generate_enhanced_sales_data()

st.title("Sales Performance Dashboard")
st.markdown("Deep dive into sales metrics across various dimensions with enhanced filtering and visualizations.")
st.markdown("---")

# --- Sidebar Filters ---
st.sidebar.header("Global Filters 🌍")

# Year Filter
all_years = sorted(df_orig['Year'].unique())
selected_years = st.sidebar.multiselect("Select Year(s)", all_years, default=all_years)

# Quarter Filter
all_quarters = sorted(df_orig[df_orig['Year'].isin(selected_years)]['Quarter'].unique())
selected_quarters = st.sidebar.multiselect("Select Quarter(s)", all_quarters, default=all_quarters)

# Region Filter
all_regions = sorted(df_orig['Region'].unique())
selected_regions = st.sidebar.multiselect("Select Region(s)", all_regions, default=all_regions)

# Product Category Filter
all_categories = sorted(df_orig['Product Category'].unique())
selected_categories = st.sidebar.multiselect("Select Product Category(s)", all_categories, default=all_categories)

# Sub-Category Filter (dependent on selected categories)
sub_cat_options = sorted(df_orig[df_orig['Product Category'].isin(selected_categories)]['Sub-Category'].unique())
selected_sub_categories = st.sidebar.multiselect("Select Sub-Category(s)", sub_cat_options, default=sub_cat_options)

# Salesperson Filter
all_salespersons = sorted(df_orig['Salesperson'].unique())
selected_salespersons = st.sidebar.multiselect("Select Salesperson(s)", all_salespersons, default=all_salespersons)


# --- Filter Data based on Selections ---
query_parts = []
if selected_years: query_parts.append("Year in @selected_years")
if selected_quarters: query_parts.append("Quarter in @selected_quarters")
if selected_regions: query_parts.append("Region in @selected_regions")
if selected_categories: query_parts.append("`Product Category` in @selected_categories") # Backticks for spaces
if selected_sub_categories: query_parts.append("`Sub-Category` in @selected_sub_categories")
if selected_salespersons: query_parts.append("Salesperson in @selected_salespersons")

if query_parts:
    df_filtered = df_orig.query(" and ".join(query_parts)).copy()
else:
    df_filtered = df_orig.copy()


if df_filtered.empty:
    st.warning("No data available for the selected filters. Please broaden your selection.")
    st.stop()

# --- Tabs for Different Views ---
tab_overview, tab_regional, tab_product, tab_salesperson, tab_detailed_data = st.tabs([
    "📊 Overview", "🗺️ Regional Analysis", "🛍️ Product Performance", "🧑‍💼 Salesperson Insights", "📄 Detailed Data"
])

with tab_overview:
    st.header("Overall Performance Snapshot")

    # Calculate KPIs
    total_revenue = df_filtered['Revenue'].sum()
    total_target = df_filtered['Target Revenue'].sum()
    total_profit = df_filtered['Profit'].sum()
    total_prev_year_revenue = df_filtered['Previous Year Revenue'].sum(skipna=True)
    avg_profit_margin = df_filtered['Profit Margin (%)'].mean() if not df_filtered.empty else 0

    revenue_vs_target_perc = ((total_revenue / total_target) - 1) * 100 if total_target else 0
    yoy_growth_perc = ((total_revenue / total_prev_year_revenue) - 1) * 100 if total_prev_year_revenue else 0

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.metric("Total Revenue", f"${total_revenue:,.0f}", f"{yoy_growth_perc:.1f}% vs PY")
    with kpi_col2:
        st.metric("Total Profit", f"${total_profit:,.0f}")
    with kpi_col3:
        st.metric("Avg. Profit Margin", f"{avg_profit_margin:.1f}%")
    with kpi_col4:
        st.metric("Revenue vs Target", f"{revenue_vs_target_perc:.1f}%", delta_color="normal" if revenue_vs_target_perc >=0 else "inverse")

    st.markdown("---")
    st.subheader("Monthly Performance Trend")
    monthly_agg = df_filtered.groupby('YearMonth')[['Revenue', 'Profit', 'Target Revenue']].sum().reset_index()
    monthly_agg['Date'] = monthly_agg['YearMonth'].dt.to_timestamp()
    fig_trend = create_line_chart(monthly_agg, 'Date', ['Revenue', 'Profit', 'Target Revenue'],
                                  "Monthly Revenue, Profit, and Target",
                                  y_labels=['Actual Revenue', 'Actual Profit', 'Target Revenue'],
                                  legend_title="Metric")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    col_treemap, col_pie = st.columns(2)
    with col_treemap:
        st.subheader("Revenue Contribution by Product Category & Sub-Category")
        # Ensure no NaN values in path for treemap
        df_tree = df_filtered.dropna(subset=['Product Category', 'Sub-Category'])
        if not df_tree.empty:
            fig_treemap = create_treemap(df_tree, ['Product Category', 'Sub-Category'], 'Revenue',
                                         "Revenue by Product Hierarchy")
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("Not enough data for Treemap with current filters.")

    with col_pie: # Using pie for limited categories for illustrative purposes
        st.subheader("Revenue by Region")
        region_sum = df_filtered.groupby('Region')['Revenue'].sum().reset_index()
        if not region_sum.empty and len(region_sum['Region'].unique()) <= 7: # Limit pie categories
             fig_pie_region = px.pie(region_sum, values='Revenue', names='Region', title="Revenue Share by Region",
                                    color_discrete_sequence=px.colors.sequential.RdBu)
             st.plotly_chart(fig_pie_region, use_container_width=True)
        else:
            st.info("Too many regions for a Pie chart or no data. Bar chart used in Regional Analysis tab.")


with tab_regional:
    st.header("Regional Performance Analysis")
    
    col_rev, col_prof = st.columns(2)
    with col_rev:
        st.subheader("Revenue by Region")
        region_revenue = df_filtered.groupby('Region')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
        fig_reg_rev = create_bar_chart(region_revenue, 'Region', 'Revenue', "Total Revenue per Region")
        st.plotly_chart(fig_reg_rev, use_container_width=True)

    with col_prof:
        st.subheader("Profit by Region")
        region_profit = df_filtered.groupby('Region')['Profit'].sum().reset_index().sort_values('Profit', ascending=False)
        fig_reg_prof = create_bar_chart(region_profit, 'Region', 'Profit', "Total Profit per Region", color_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_reg_prof, use_container_width=True)

    st.markdown("---")
    col_yoy, col_target = st.columns(2)
    with col_yoy:
        st.subheader("YoY Revenue Growth by Region (%)")
        # Need to handle cases where previous year revenue might be zero or NaN for a region
        # We'll sum current and previous year revenue by region first
        current_year_revenue_region = df_filtered.groupby('Region')['Revenue'].sum()
        prev_year_revenue_region = df_filtered.groupby('Region')['Previous Year Revenue'].sum()
        
        yoy_region_df = pd.DataFrame({
            'Current Revenue': current_year_revenue_region,
            'Previous Revenue': prev_year_revenue_region
        }).reset_index()
        
        yoy_region_df['YoY Growth (%)'] = ((yoy_region_df['Current Revenue'] / yoy_region_df['Previous Revenue']) - 1) * 100
        yoy_region_df.replace([np.inf, -np.inf], np.nan, inplace=True) # Handle division by zero/NaN
        yoy_region_df.dropna(subset=['YoY Growth (%)'], inplace=True)

        if not yoy_region_df.empty:
            fig_reg_yoy = create_bar_chart(yoy_region_df.sort_values('YoY Growth (%)', ascending=False), 
                                           'Region', 'YoY Growth (%)', "YoY Revenue Growth by Region")
            st.plotly_chart(fig_reg_yoy, use_container_width=True)
        else:
            st.info("Not enough data for YoY Regional Growth (ensure previous year data exists).")


    with col_target:
        st.subheader("Revenue vs. Target by Region (%)")
        region_target_perf = df_filtered.groupby('Region').agg(
            TotalRevenue=('Revenue', 'sum'),
            TotalTarget=('Target Revenue', 'sum')
        ).reset_index()
        region_target_perf['Vs Target (%)'] = ((region_target_perf['TotalRevenue'] / region_target_perf['TotalTarget']) - 1) * 100
        region_target_perf.replace([np.inf, -np.inf], np.nan, inplace=True)
        region_target_perf.dropna(subset=['Vs Target (%)'], inplace=True)
        
        if not region_target_perf.empty:
            fig_reg_target = create_bar_chart(region_target_perf.sort_values('Vs Target (%)', ascending=False),
                                              'Region', 'Vs Target (%)', "Revenue vs. Target Performance by Region")
            fig_reg_target.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Target Line")
            st.plotly_chart(fig_reg_target, use_container_width=True)
        else:
            st.info("Not enough data for Regional Target Performance.")


with tab_product:
    st.header("Product Performance Analysis")
    
    st.subheader("Performance by Product Category")
    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        cat_revenue = df_filtered.groupby('Product Category')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)
        fig_cat_rev = create_bar_chart(cat_revenue, 'Product Category', 'Revenue', "Revenue by Product Category")
        st.plotly_chart(fig_cat_rev, use_container_width=True)
    with cat_col2:
        cat_profit = df_filtered.groupby('Product Category')['Profit'].sum().reset_index().sort_values('Profit', ascending=False)
        fig_cat_prof = create_bar_chart(cat_profit, 'Product Category', 'Profit', "Profit by Product Category", color_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_cat_prof, use_container_width=True)

    st.markdown("---")
    st.subheader("Performance by Sub-Category (Top 15 by Revenue)")
    subcat_col1, subcat_col2 = st.columns(2)
    top_n_subcategories = 15
    with subcat_col1:
        subcat_revenue = df_filtered.groupby('Sub-Category')['Revenue'].sum().nlargest(top_n_subcategories).reset_index()
        fig_subcat_rev = create_bar_chart(subcat_revenue, 'Sub-Category', 'Revenue', f"Top {top_n_subcategories} Sub-Categories by Revenue")
        st.plotly_chart(fig_subcat_rev, use_container_width=True)
    with subcat_col2:
        subcat_profit = df_filtered.groupby('Sub-Category')['Profit'].sum().nlargest(top_n_subcategories).reset_index()
        fig_subcat_prof = create_bar_chart(subcat_profit, 'Sub-Category', 'Profit', f"Top {top_n_subcategories} Sub-Categories by Profit", color_sequence=px.colors.qualitative.Pastel1)
        st.plotly_chart(fig_subcat_prof, use_container_width=True)

    st.markdown("---")
    st.subheader("Product Portfolio Analysis: Units Sold vs. Profit Margin by Sub-Category")
    # Aggregate to Sub-Category level
    portfolio_data = df_filtered.groupby('Sub-Category').agg(
        TotalUnits=('Units Sold', 'sum'),
        AvgProfitMargin=('Profit Margin (%)', 'mean'),
        TotalRevenue=('Revenue', 'sum') # For bubble size
    ).reset_index().dropna()

    if not portfolio_data.empty and len(portfolio_data) > 1 : # Scatter needs at least 2 points
        fig_portfolio = px.scatter(portfolio_data, x='TotalUnits', y='AvgProfitMargin',
                                   size='TotalRevenue', color='Sub-Category',
                                   hover_name='Sub-Category',
                                   title="Sub-Category Performance: Units vs. Profit Margin (Bubble size: Revenue)",
                                   labels={'TotalUnits': 'Total Units Sold', 'AvgProfitMargin': 'Average Profit Margin (%)'})
        fig_portfolio.update_layout(showlegend=True) # Show legend for color if many sub-cats
        st.plotly_chart(fig_portfolio, use_container_width=True)
    else:
        st.info("Not enough data for Product Portfolio scatter plot.")


with tab_salesperson:
    st.header("Salesperson Performance Insights")

    top_n_salespersons = 10
    sales_col1, sales_col2 = st.columns(2)
    with sales_col1:
        st.subheader(f"Top {top_n_salespersons} Salespersons by Revenue")
        sales_revenue = df_filtered.groupby('Salesperson')['Revenue'].sum().nlargest(top_n_salespersons).reset_index()
        fig_sales_rev = create_bar_chart(sales_revenue, 'Salesperson', 'Revenue', "Salesperson Revenue")
        st.plotly_chart(fig_sales_rev, use_container_width=True)
    with sales_col2:
        st.subheader(f"Top {top_n_salespersons} Salespersons by Profit")
        sales_profit = df_filtered.groupby('Salesperson')['Profit'].sum().nlargest(top_n_salespersons).reset_index()
        fig_sales_prof = create_bar_chart(sales_profit, 'Salesperson', 'Profit', "Salesperson Profit", color_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_sales_prof, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Salesperson Average Deal Size and Profit Margin")
    sales_agg = df_filtered.groupby('Salesperson').agg(
        AvgRevenuePerDeal=('Revenue', 'mean'),
        AvgProfitMargin=('Profit Margin (%)', 'mean'),
        TotalDeals=('Revenue', 'count') # For bubble size
    ).reset_index().dropna()
    
    if not sales_agg.empty and len(sales_agg) > 1:
        fig_sales_scatter = px.scatter(sales_agg, x='AvgRevenuePerDeal', y='AvgProfitMargin',
                                       size='TotalDeals', color='Salesperson',
                                       hover_name='Salesperson',
                                       title="Salesperson: Avg Deal Size vs. Avg Profit Margin (Bubble size: Total Deals)",
                                       labels={'AvgRevenuePerDeal': 'Average Revenue per Deal ($)',
                                               'AvgProfitMargin': 'Average Profit Margin (%)'})
        st.plotly_chart(fig_sales_scatter, use_container_width=True)
    else:
        st.info("Not enough data for Salesperson scatter plot.")

with tab_detailed_data:
    st.header("Filtered Detailed Data")
    st.info("Displaying a sample of the filtered data. For full data export, consider adding an export button (not implemented here).")
    
    # Define columns to display and their formatting
    display_columns = [
        'Date', 'Year', 'Quarter', 'Region', 'Product Category', 'Sub-Category', 'Salesperson',
        'Revenue', 'Units Sold', 'Target Revenue', 'COGS', 'Profit',
        'Revenue vs Target (%)', 'YoY Revenue Growth (%)', 'Profit Margin (%)'
    ]
    
    # Ensure all display columns exist in df_filtered, add them with NaN if not (should not happen with query)
    for col in display_columns:
        if col not in df_filtered.columns:
            df_filtered[col] = np.nan
            
    df_display = df_filtered[display_columns].copy()

    # Apply formatting for better readability
    format_dict = {
        "Revenue": "${:,.2f}", "Target Revenue": "${:,.2f}", "COGS": "${:,.2f}", "Profit": "${:,.2f}",
        "Revenue vs Target (%)": "{:.1f}%", "YoY Revenue Growth (%)": "{:.1f}%", "Profit Margin (%)": "{:.1f}%"
    }
    # Only apply formatting to columns that exist in df_display
    valid_format_dict = {k: v for k, v in format_dict.items() if k in df_display.columns}

    st.dataframe(
        df_display.head(1000).style.format(valid_format_dict, na_rep="-"), # Show up to 1000 rows, format NaNs
        use_container_width=True,
        hide_index=True
    )

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.info("Advanced Sales Dashboard v2.0. Uses simulated data.")
st.sidebar.markdown("Developed for INDIVIDUAL ACTIVITY 3.")
