# Streamlit Sales Performance Dashboard

This project demonstrates a sales performance dashboard built using Streamlit, Pandas, and Plotly. It showcases the application of data visualization principles and cognitive factors for effective decision support, based on materials from INDIVIDUAL ACTIVITY 3.

The dashboard uses **simulated data** for demonstration purposes.

## Features

*   Interactive filtering by Date Range, Region, and Product Category.
*   KPIs displaying overall performance (Total Revenue, Revenue vs Target, Units Sold) with comparisons (YoY Growth).
*   Bar charts comparing performance across Regions and Product Categories.
*   Line chart showing Revenue and Target Revenue trends over time.
*   Expandable detailed data table.

## Setup and Running

1.  **Prerequisites:**
    *   Python 3.8+ installed.
    *   `pip` (Python package installer).
    *   `venv` (Recommended for managing virtual environments).

2.  **Clone or Download:**
    *   Get the project files (`sales_dashboard.py`, `rationale.md`, `requirements.txt`, `README.md`) into a local directory.

3.  **Create Virtual Environment (Recommended):**
    *   Open your terminal or command prompt.
    *   Navigate to the project directory:
        ```bash
        cd path/to/streamlit_sales_dashboard
        ```
    *   Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    *   Activate the virtual environment:
        *   **Windows:** `.\venv\Scripts\activate`
        *   **macOS/Linux:** `source venv/bin/activate`
        (You should see `(venv)` preceding your prompt).

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
    *   Streamlit will start the server, and the dashboard should automatically open in your default web browser. If not, the terminal will provide local and network URLs you can navigate to.

6.  **Using the Dashboard:**
    *   Use the filters in the left sidebar to select the desired date range, regions, and product categories.
    *   The dashboard content (KPIs, charts, table) will update automatically based on your selections.
    *   Hover over chart elements for detailed tooltips.
    *   Expand the "View Detailed Data" section to see the underlying filtered data.

7.  **Stopping the App:**
    *   Go back to your terminal where Streamlit is running and press `Ctrl + C`.

8.  **Deactivate Virtual Environment (Optional):**
    *   When you're finished, you can deactivate the virtual environment by simply typing:
        ```bash
        deactivate
        ```

## Rationale

Please refer to the `rationale.md` file for a detailed explanation of the design decisions based on cognitive principles and data visualization best practices.