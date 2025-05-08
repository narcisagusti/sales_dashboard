# Streamlit Sales Performance Dashboard

This project presents a significantly enhanced sales performance dashboard built using Streamlit, Pandas, and Plotly. It's designed to showcase advanced application of data visualization principles and cognitive factors for robust business decision support, as per INDIVIDUAL ACTIVITY 3.

The dashboard uses **simulated, granular data** including product sub-categories, salespersons, and profitability metrics.

## Key Features

*   **Tabbed Interface:** Organized views for "Overview", "Regional Analysis", "Product Performance", "Salesperson Insights", and "Detailed Data".
*   **Advanced Global Filters:**
    *   Year(s)
    *   Quarter(s)
    *   Region(s)
    *   Product Category(s)
    *   Sub-Category(s)
    *   Salesperson(s)
*   **Comprehensive KPIs:** Total Revenue, Total Profit, Average Profit Margin, Revenue vs Target, YoY Growth.
*   **In-Depth Visualizations:**
    *   Monthly trends for Revenue, Profit, and Targets.
    *   Treemaps for hierarchical contribution analysis (Product Category & Sub-Category).
    *   Bar charts for Revenue, Profit, YoY Growth %, and Revenue vs. Target % across Regions, Product Categories, Sub-Categories, and Salespersons.
    *   Scatter plots for portfolio analysis (e.g., Units Sold vs. Profit Margin by Sub-Category; Avg Deal Size vs. Avg Profit Margin by Salesperson).
*   **Detailed Data View:** A filterable and formatted table of the underlying data.
*   **Modular Code:** Improved code structure with helper functions for plotting.

## Setup and Running

1.  **Prerequisites:**
    *   Python 3.8+ installed.
    *   `pip` (Python package installer).
    *   `venv` (Recommended for managing virtual environments).

2.  **Clone or Download:**
    *   Get the project files (`sales_dashboard.py`, `rationale.md`, `requirements.txt`, `README.md`, `.gitignore`) into a local directory.

3.  **Create Virtual Environment (Recommended):**
    *   Open your terminal or command prompt.
    *   Navigate to the project directory:
        ```bash
        cd path/to/your_project_folder
        ```
    *   Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    *   Activate the virtual environment:
        *   **Windows:** `.\venv\Scripts\activate`
        *   **macOS/Linux:** `source venv/bin/activate`

4.  **Install Dependencies:**
    *   With the virtual environment activated, install the required packages:
        ```bash
        pip install -r requirements.txt
        ```

5.  **Run the Streamlit App:**
    *   Execute the following command in your terminal:
        ```bash
        streamlit run sales_dashboard.py
        ```
    *   Streamlit will start the server, and the dashboard should automatically open in your default web browser.

6.  **Using the Dashboard:**
    *   Navigate through the different tabs to explore various analytical perspectives.
    *   Use the comprehensive filters in the left sidebar to narrow down the data.
    *   Interact with charts (hover for tooltips, zoom where applicable).
    *   The "Detailed Data" tab provides a view of the raw, filtered data.

7.  **Stopping the App:**
    *   Go back to your terminal where Streamlit is running and press `Ctrl + C`.

## Rationale for Design

Please refer to the `rationale.md` file for an extensive explanation of the design decisions, linking them to cognitive principles, data visualization best practices, and strategies for mitigating cognitive biases.