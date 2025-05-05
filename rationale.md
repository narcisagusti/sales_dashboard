# Rationale for Sales Performance Dashboard Design

This document outlines the design decisions made for the Streamlit Sales Performance Dashboard, grounding them in the cognitive principles and data visualization best practices discussed in the provided course materials ("Cognitive Principles for Dashboard Design", "Cognitive Biases in Decision Making", "Data Visualization Principles").

## 1. Overall Goal & Target User

*   **Goal:** To provide sales managers and stakeholders with a clear, interactive tool to understand sales performance, identify trends and exceptions, compare results against targets and historical data, and support informed decision-making regarding resource allocation, strategy adjustments, and performance evaluation.
*   **User:** Sales managers, regional managers, potentially VPs or analysts who need quick insights into performance drivers.

## 2. Dashboard Structure and Layout

*   **Decision:** A multi-section layout with sidebar filters, top-level KPIs, comparative charts, a trend chart, and a detailed data table within an expander.
*   **Rationale:**
    *   **Decision Hierarchy (Doc 1, Pg 4):** The layout follows a logical flow from high-level summary (KPIs) to more detailed breakdowns (regions, products) and trends, mimicking a natural decision-making process: 1. How are we doing overall? -> 2. Where are the key variations? -> 3. How is performance changing over time? -> 4. Let me see the details.
    *   **Visual Hierarchy (Doc 3, Pg 5):** KPIs are placed at the top with larger font sizes (`st.metric`) to immediately draw attention to the most critical summary figures. Section headers (`st.header`, `st.subheader`) guide the user through different analytical perspectives. Consistent spacing and alignment create a clean structure.
    *   **Cognitive Load Management (Doc 1, Pg 1):** Information is chunked into logical sections (KPIs, Regions, Products, Trend, Details). Filters in the sidebar allow users to reduce the amount of information displayed at once, minimizing *Extraneous Cognitive Load* and allowing focus on relevant segments.
    *   **Working Memory Optimization (Doc 1, Pg 2):** Presenting only 3 key KPIs prominently respects the limited capacity of working memory (4-7 items). Filters help manage the information load when exploring specific segments. The sidebar provides *External Memory Aids* for the current filter context.
    *   **Progressive Disclosure (Doc 3, Pg 4):** The detailed data table is placed within an `st.expander`. This keeps the initial view focused on high-level visualizations (reducing initial cognitive load) while allowing users to access granular data *on demand* when needed for deeper investigation.

## 3. Filters (Sidebar)

*   **Decision:** Use sidebar for Date Range, Region, and Product Category filters with multi-select options and defaults set to "All".
*   **Rationale:**
    *   **Cognitive Offloading (Doc 1, Pg 1):** Filters allow users to interactively tailor the view to their specific questions, offloading the mental effort of filtering data manually or remembering specific subset values.
    *   **Anchoring Bias Mitigation (Doc 2, Pg 2):** Providing filters allows users to start their analysis from different perspectives (e.g., focusing on a specific region first) rather than being anchored by a single default view (like only showing the top-performing region initially). Defaulting to "All" provides an unbiased starting overview.
    *   **Working Memory Optimization (Doc 1, Pg 2):** Filters reduce the amount of data being processed and visualized, making it easier to hold relevant information in mind for the current analysis task.

## 4. Key Performance Indicators (KPIs)

*   **Decision:** Display Total Revenue, Revenue vs Target (%), and Total Units Sold prominently using `st.metric`, including relevant deltas (YoY growth, Target value).
*   **Rationale:**
    *   **Situational Awareness (Decision Hierarchy - Doc 1, Pg 4):** These KPIs provide an immediate snapshot of the overall business health ("How are we doing?").
    *   **Visual Hierarchy (Doc 3, Pg 5):** Using `st.metric` with its distinct styling and placement at the top emphasizes their importance.
    *   **Comparative Analysis (Doc 1, Pg 5) & Contextual Reference Points (Doc 3, Pg 6):** Displaying revenue alongside YoY growth (%) and performance against target (%) provides crucial context. Absolute numbers alone are less meaningful than relative performance. The target value is explicitly shown in the delta for the "Revenue vs Target" metric.
    *   **Recency Bias Mitigation (Doc 2, Pg 6):** Including Year-over-Year (YoY) growth alongside the current total revenue prevents over-reliance on the most recent absolute numbers by providing historical context.
    *   **Framing Effect Mitigation (Doc 2, Pg 4):** Presenting both absolute revenue and relative metrics (vs. Target, vs. PY) provides a more balanced view than showing only one frame (e.g., just the percentage gain/loss). Labels are neutral ("Total Revenue", "Revenue vs Target").

## 5. Bar Charts (Revenue by Region / Product Category)

*   **Decision:** Use separate bar charts to show total revenue aggregated by region and product category. Sorted descending.
*   **Rationale:**
    *   **Chart Type Appropriateness (Doc 3, Pg 2):** Bar charts are ideal for comparing discrete categorical data (regions, product categories) based on a quantitative measure (revenue). The length encoding is easily perceived for comparison.
    *   **Comparative Analysis (Doc 1, Pg 5):** These charts directly facilitate comparison *between* categories, helping users identify top and bottom performers (*Exception Identification* from Decision Hierarchy). Sorting helps quickly identify the highest contributors.
    *   **Preattentive Processing (Doc 3, Pg 3):** While not heavily relying on color for quantitative encoding here, the distinct bars and their lengths allow for rapid visual comparison of magnitudes. Consistent, non-distracting colors (`px.colors.qualitative.Pastel`) are used. Text labels (`text_auto`) improve readability without clutter.
    *   **Data-Ink Ratio (Doc 3, Pg 1):** The charts are kept clean: no unnecessary 3D effects, gradients, or excessive gridlines. Axis titles are simplified where the main title provides context (e.g., removing x-axis title when categories are clear).

## 6. Line Chart (Revenue Trend Over Time)

*   **Decision:** Use a line chart to display monthly Revenue and Target Revenue over the selected time period.
*   **Rationale:**
    *   **Pattern Recognition Support (Doc 1, Pg 3):** Line charts excel at showing trends, seasonality, and patterns over continuous intervals (time). Users can quickly perceive upward/downward trends and seasonal fluctuations.
    *   **Chart Type Appropriateness (Doc 3, Pg 2):** Line charts are the standard and most effective choice for visualizing time-series data.
    *   **Contextual Reference Points (Doc 3, Pg 6):** Plotting Actual Revenue alongside the Target Revenue line provides immediate visual context for performance against goals over time.
    *   **Availability Bias / Recency Bias Mitigation (Doc 2, Pg 3 & 6):** Displaying the trend over the *entire selected period* counteracts the tendency to overemphasize the most recent data points. Visualizing seasonality helps avoid misinterpreting cyclical dips as new negative trends.
    *   **Consistent Visual Language (Doc 3, Pg 7):** Consistent colors are used (blue for actual, grey/dashed for target) making the lines easy to distinguish across potential reruns or different filter views.

## 7. Data Table (Detailed View)

*   **Decision:** Include a detailed data table within an `st.expander`, showing key metrics and calculated fields, formatted for readability.
*   **Rationale:**
    *   **Progressive Disclosure (Doc 3, Pg 4):** Provides access to granular data for users who need to investigate specific figures or export data, without cluttering the primary visual interface.
    *   **Cognitive Offloading (Doc 1, Pg 1):** Serves as an external reference for specific values without requiring the user to memorize them from the charts.
    *   **Transparency:** Allows users to see the underlying data that feeds the visualizations, building trust.
    *   **Survivorship Bias Mitigation (Implicit - Doc 2, Pg 7):** By showing the full filtered dataset, it ensures (assuming the underlying data generation is complete) that users aren't just seeing data from "surviving" entities if the context involved tracking entities that could drop out (like specific products being discontinued - though not explicitly modeled here). Formatting enhances readability, reducing cognitive load when scanning the table.

## 8. Color Usage

*   **Decision:** Use qualitative color palettes (e.g., `px.colors.qualitative.Pastel`) for categorical distinctions (regions, products) and distinct, conventional colors for time series lines (blue for actual, grey for target). Avoid using red/green for performance states in charts initially to avoid potential misinterpretation or color vision deficiency issues, relying more on position and value labels. `st.metric` uses default red/green for deltas which is a common convention.
*   **Rationale:**
    *   **Preattentive Processing (Doc 3, Pg 3):** Color helps distinguish categories in bar charts and lines in the trend chart. Using softer palettes avoids overwhelming the user.
    *   **Consistent Visual Language (Doc 3, Pg 7):** A consistent approach to color application helps users quickly understand what different colors represent across the dashboard.
    *   **Framing Effect / Accessibility:** Avoiding strong red/green performance indicators in the main charts (except `st.metric` delta) provides a more neutral view and is more accessible for users with color vision deficiencies. Performance is primarily communicated through position (bar height), explicit values, and comparison lines (target).

By integrating these principles, the dashboard aims to be not just informative but also efficient and effective, reducing cognitive load, mitigating potential biases, and ultimately supporting better business decisions.