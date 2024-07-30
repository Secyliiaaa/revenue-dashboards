# -*- coding: utf-8 -*-
"""revenue_app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HFUrQ4XUaIo7-O-S7IERVszFm503fO6i
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
file_path = 'iconnet-revenue.xlsx'
data = pd.read_excel(file_path, sheet_name='actual data')

# Preprocess the data
data['tanggal'] = pd.to_datetime(data['tanggal'])
data['tahun'] = data['tanggal'].dt.year
data['month'] = data['tanggal'].dt.strftime('%Y-%m')

# Sum revenue by month for each category
revenue_by_province = data.groupby(['month', 'namakp'])['totalharga'].sum().unstack().fillna(0)
revenue_by_product = data.groupby(['month', 'namaproduk'])['totalharga'].sum().unstack().fillna(0)
revenue_by_agent = data.groupby(['month', 'mitraagen'])['totalharga'].sum().unstack().fillna(0)
revenue_by_ae = data.groupby(['month', 'ae'])['totalharga'].sum().unstack().fillna(0)

# Data harga paket ICONNET di 2022 dan 2023 
data_harga = {
    'Provinsi': ['BALI', 'BALI', 'BALI', 'BALI', 'BALI', 
                 'NUSA TENGGARA TIMUR', 'NUSA TENGGARA TIMUR', 'NUSA TENGGARA TIMUR', 'NUSA TENGGARA TIMUR', 'NUSA TENGGARA TIMUR', 
                 'NUSA TENGGARA BARAT', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA BARAT'] * 4,
    'Nama_Layanan': ['ICONNET 10 MBPS', 'ICONNET 20 MBPS', 'ICONNET 35 MBPS', 'ICONNET 50 MBPS', 'ICONNET 100 MBPS',
                     'ICONNET 10 MBPS', 'ICONNET 20 MBPS', 'ICONNET 35 MBPS', 'ICONNET 50 MBPS', 'ICONNET 100 MBPS',
                     'ICONNET 10 MBPS', 'ICONNET 20 MBPS', 'ICONNET 35 MBPS', 'ICONNET 50 MBPS', 'ICONNET 100 MBPS'] * 4,
    'Agen': ['iconplus', 'iconplus', 'iconplus', 'iconplus', 'iconplus',
             'haleyora', 'haleyora', 'haleyora', 'haleyora', 'haleyora',
             'kinarya', 'kinarya', 'kinarya', 'kinarya', 'kinarya',
             'saputra', 'saputra', 'saputra', 'saputra', 'saputra'] * 3,
    'Harga_2022': [140000, 188000, 230000, 336000, 536000, 
                   166500, 217560, 290000, 459540, 753690,
                   150000, 196000, 290000, 414000, 679000,
                   150000, 196000, 290000, 414000, 679000] * 3,
    'Harga_2023': [188000, 212000, 230000, 336000, 536000, 
                   196000, 287000, 290000, 414000, 679000,
                   196000, 287000, 290000, 414000, 679000,
                   196000, 287000, 290000, 414000, 679000] * 3
}

# Convert dictionary to DataFrame
df_harga = pd.DataFrame(data_harga)

# Define features and targets for harga
X_harga = df_harga[['Harga_2022', 'Harga_2023']].values

# Generate targets for 2024, 2025, and 2026 with assumed growth rates
np.random.seed(42)
y_harga_2024 = (df_harga['Harga_2023'] * np.random.uniform(1.05, 1.15, df_harga.shape[0])).astype(int)
y_harga_2025 = (y_harga_2024 * np.random.uniform(1.05, 1.15, df_harga.shape[0])).astype(int)
y_harga_2026 = (y_harga_2025 * np.random.uniform(1.05, 1.15, df_harga.shape[0])).astype(int)

# Train decision tree models for harga
model_harga_2024 = DecisionTreeRegressor(random_state=42)
model_harga_2024.fit(X_harga, y_harga_2024)

model_harga_2025 = DecisionTreeRegressor(random_state=42)
model_harga_2025.fit(X_harga, y_harga_2025)

model_harga_2026 = DecisionTreeRegressor(random_state=42)
model_harga_2026.fit(X_harga, y_harga_2026)

# Predict future harga
df_harga['pred_harga_2024'] = model_harga_2024.predict(X_harga).astype(int)
df_harga['pred_harga_2025'] = model_harga_2025.predict(X_harga).astype(int)
df_harga['pred_harga_2026'] = model_harga_2026.predict(X_harga).astype(int)

# Data for actual and predicted revenue
data_2022 = {
    'Province': ['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR'],
    '2022': [3220853684, 1277415042, 604448722]
}

data_2023 = {
    'Province': ['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR'],
    '2023': [9086408000, 3143802000, 3672627000]
}

predicted_data = {
    'Province': ['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR'],
    '2024': [322194404700, 120537268425, 92469032460],
    '2025': [346179942900, 129510581475, 99352825220],
    '2026': [371602158300, 139021374825, 106648940940]
}

df_actual_2022 = pd.DataFrame(data_2022).set_index('Province')
df_actual_2023 = pd.DataFrame(data_2023).set_index('Province')
df_pred = pd.DataFrame(predicted_data).set_index('Province')

# Function to format revenue in millions
def format_revenue_million(revenue):
    return f"Rp {revenue / 1_000_000:.2f}M"

# Function to calculate percentage change
def calculate_percentage_change(current, previous):
    return ((current - previous) / previous) * 100

# Streamlit Dashboard
image = 'logo123.png'
st.sidebar.image(image, use_column_width=True)

with st.sidebar:
    st.title('Dashboard Revenue ICONNET')
    page = st.radio(
        "Select Page",
        ["Dashboard", "Actual Data", "Predictor"],
        index=0,
        key="main_menu"
    )

# Custom CSS for sidebar and titles
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        font-size: 18px;
    }
    .sidebar .sidebar-content h2 {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .sidebar .sidebar-content label {
        font-size: 20px;
        margin-bottom: 10px;
    }
    .sidebar .sidebar-content .stRadio {
        margin-bottom: 20px;
    }
    .stRadio > div {
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .plotly-tooltip {
        font-size: 14px !important;
        font-family: Arial, sans-serif !important.
    }
    .title-line {
        position: relative;
        display: inline-block;
        font-size: 40px;
        font-weight: bold.
        margin-top: 5px;
        margin-bottom: 20px;
    }
    .title-line::after {
        content: '';
        display: block.
        width: 100%.
        height: 4px.
        background: rgba(0, 0, 0, 0.1).
        margin-top: 20px.
        border-radius: 2px.
    }
    .stSelectbox option[value=""] { /* Target the placeholder option */
        color: #888; /* Make the text lighter */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------

if page == "Dashboard":
    st.markdown('<h1 class="title-line">Dashboard Revenue ICONNET</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        actual_year = st.selectbox("Select Actual Year", ["2022", "2023"])
        df_actual_year = df_actual_2022 if actual_year == "2022" else df_actual_2023
        fig_actual = go.Figure()

        # Add bar chart for actual data
        fig_actual.add_trace(go.Bar(
            x=[0, 1, 2],
            y=df_actual_year[actual_year],
            name=f"Actual Revenue {actual_year}",
            marker_color='blue',
            hovertemplate="<br>".join([
                "Year: " + actual_year,
                "Province: %{x}",
                "Revenue: Rp %{y:,.2f}"
            ])
        ))

        fig_actual.update_layout(
            title=dict(
                text=f"Actual Revenue for {actual_year}"
            ),
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2],
                ticktext=['BALI', 'NTB', 'NTT']
            ),
            yaxis=dict(
                title="Revenue (Rp)",
                tickformat=',.0f',
                titlefont=dict(size=14)
            ),
            legend_title="Province",
            barmode='group',
            width=600,
            height=500
        )

        st.plotly_chart(fig_actual, use_container_width=True)

    with col2:
        prediction_year = st.selectbox("Select Prediction Year", ["2024", "2025", "2026"])
        fig_pred = go.Figure()

        # Add bar chart for predicted data
        fig_pred.add_trace(go.Bar(
            x=df_pred.index,
            y=df_pred[prediction_year],
            name=f"Predicted Revenue {prediction_year}",
            marker_color='yellow',
            hovertemplate="<br>".join([
                "Year: " + prediction_year,
                "Province: %{x}",
                "Revenue: Rp %{y:,.2f}"
            ])
        ))

        fig_pred.update_layout(
            title=dict(
                text=f"Predicted Revenue for {prediction_year}"
            ),
            xaxis=dict(
                tickmode='array',
                tickvals=['BALI', 'NUSA TENGGARA BARAT', 'NUSA TENGGARA TIMUR'], # Sesuaikan dengan indeks DataFrame df_pred
                ticktext=['BALI', 'NTB', 'NTT'] # Ubah label provinsi
            ),
            yaxis=dict(
                title="Revenue (Rp)",
                tickformat=',.0f',
                titlefont=dict(size=14)
            ),
            legend_title="Province",
            barmode='group',
            width=600,
            height=500
        )

        st.plotly_chart(fig_pred, use_container_width=True)

    total_predicted_revenue = df_pred[prediction_year].sum()
    total_actual_revenue = df_actual_year[actual_year].sum()
    percentage_change = calculate_percentage_change(total_predicted_revenue, total_actual_revenue)

    st.metric(
        label="Overall Revenue",
        value=f"Rp {total_predicted_revenue:,.2f}",
        delta=f"{percentage_change:.2f} %",
        delta_color="normal",
        help="This represents the total predicted revenue for the selected year and the percentage change compared to the selected actual year."
    )

    # Display quick insights
    st.markdown(
        f"""
        <div class="insight-box">
              <h3>Informations</h3>
              <p><b>Total Revenue for {prediction_year}:</b> Rp {total_predicted_revenue:,.2f}</p>
              <p><b>Percentage Change compared to {actual_year}:</b> {percentage_change:.2f} %</p>
              <p><b>Province Comparison:</b></p>
              <ul>
                  <li><b>BALI:</b> Rp {df_pred.at['BALI', prediction_year]:,.2f} ({calculate_percentage_change(df_pred.at['BALI', prediction_year], df_actual_year.at['BALI', actual_year]):.2f} %)</li>
                  <li><b>NUSA TENGGARA BARAT:</b> Rp {df_pred.at['NUSA TENGGARA BARAT', prediction_year]:,.2f} ({calculate_percentage_change(df_pred.at['NUSA TENGGARA BARAT', prediction_year], df_actual_year.at['NUSA TENGGARA BARAT', actual_year]):.2f} %)</li>
                  <li><b>NUSA TENGGARA TIMUR:</b> Rp {df_pred.at['NUSA TENGGARA TIMUR', prediction_year]:,.2f} ({calculate_percentage_change(df_pred.at['NUSA TENGGARA TIMUR', prediction_year], df_actual_year.at['NUSA TENGGARA TIMUR', actual_year]):.2f} %)</li>
              </ul>
        </div>
        """, unsafe_allow_html=True
    )

    # Prepare data for download
    dashboard_table = pd.DataFrame({
        'Province': df_pred.index,
        'Actual Year': actual_year,
        'Predicted Year': prediction_year,
        'Actual Revenue': df_actual_year[actual_year],
        'Predicted Revenue': df_pred[prediction_year],
        'Percentage Change': [
            f"{100 * calculate_percentage_change(df_pred.at[prov, prediction_year], df_actual_year.at[prov, actual_year]):.2f}%"
            for prov in df_pred.index
        ]
    })

    # Add Download button for dashboard data
    csv_dashboard = dashboard_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Dashboard Data",
        data=csv_dashboard,
        file_name='dashboard_revenue_data.csv',
        mime='text/csv'
    )

# ------------------------------------------------------------------------------

elif page == "Actual Data":
    st.markdown('<h1 class="title-line">Actual Data Revenue of 2023</h1>', unsafe_allow_html=True)

    fig_province = go.Figure()
    fig_product = go.Figure()
    fig_agent = go.Figure()
    fig_ae = go.Figure()

    for province in revenue_by_province.columns:
        fig_province.add_trace(
            go.Scatter(
                x=revenue_by_province.index,
                y=revenue_by_province[province],
                mode='lines+markers',
                name=province,
                hovertemplate="<br>".join(
                    [
                        "Month: %{x}",
                        "Revenue: Rp %{y:,.2f}",
                        "Province: " + province,
                    ]
                )
            )
        )

    for product in revenue_by_product.columns:
        fig_product.add_trace(
            go.Scatter(
                x=revenue_by_product.index,
                y=revenue_by_product[product],
                mode='lines+markers',
                name=product,
                hovertemplate="<br>".join(
                    [
                        "Month: %{x}",
                        "Revenue: Rp %{y:,.2f}",
                        "Product: " + product,
                    ]
                )
            )
        )

    for agent in revenue_by_agent.columns:
        fig_agent.add_trace(
            go.Scatter(
                x=revenue_by_agent.index,
                y=revenue_by_agent[agent],
                mode='lines+markers',
                name=agent,
                hovertemplate="<br>".join(
                    [
                        "Month: %{x}",
                        "Revenue: Rp %{y:,.2f}",
                        "Agent: " + agent,
                    ]
                )
            )
        )

    for ae in revenue_by_ae.columns:
        fig_ae.add_trace(
            go.Scatter(
                x=revenue_by_ae.index,
                y=revenue_by_ae[ae],
                mode='lines+markers',
                name=ae,
                hovertemplate="<br>".join(
                    [
                        "Month: %{x}",
                        "Revenue: Rp %{y:,.2f}",
                        "AE: " + ae,
                    ]
                )
            )
        )

    # Update layout and axes for all figures
    def update_layout(fig, title, legend_title):
        fig.update_layout(
            title=dict(text=title, font=dict(size=20, color='black', family="Arial", weight="bold")),
            xaxis=dict(title="Month", tickmode='array', tickvals=revenue_by_province.index,
                       ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
            yaxis=dict(
                title="Revenue (Rp)",
                tickformat=',.0f',
                titlefont=dict(size=14)
            ),
            legend=dict(title=legend_title, x=1, y=1.02, xanchor="left"),
            width=850,
            height=500,
            margin=dict(l=20, r=20, t=50, b=20)
        )

    update_layout(fig_province, "Revenue by Province", "Province")
    update_layout(fig_product, "Revenue by Name of Product", "Product")
    update_layout(fig_agent, "Revenue by Agent Partner", "Agent")
    update_layout(fig_ae, "Revenue by Account Executive", "AE")

    # Display figures
    st.plotly_chart(fig_province, use_container_width=True)
    csv_province = revenue_by_province.to_csv().encode('utf-8')
    st.download_button(label="Download Data (Province)", data=csv_province, file_name='revenue_by_province.csv', mime='text/csv')

    st.plotly_chart(fig_product, use_container_width=True)
    csv_product = revenue_by_product.to_csv().encode('utf-8')
    st.download_button(label="Download Data (Product)", data=csv_product, file_name='revenue_by_product.csv', mime='text/csv')

    st.plotly_chart(fig_agent, use_container_width=True)
    csv_agent = revenue_by_agent.to_csv().encode('utf-8')
    st.download_button(label="Download Data (Agent)", data=csv_agent, file_name='revenue_by_agent.csv', mime='text/csv')

    st.plotly_chart(fig_ae, use_container_width=True)
    csv_ae = revenue_by_ae.to_csv().encode('utf-8')
    st.download_button(label="Download Data (AE)", data=csv_ae, file_name='revenue_by_ae.csv', mime='text/csv')

# ------------------------------------------------------------------------------

elif page == "Predictor":
    st.markdown('<h1 class="title-line">Future Price Predictor</h1>', unsafe_allow_html=True)

    # Selectors for prediction inputs with placeholder text
    prediction_year = st.selectbox(
        "Prediction Year",
        [""] + ["2024", "2025", "2026"],
        index=0,
        format_func=lambda x: "Select year..." if x == "" else x
    )
    province = st.selectbox(
        "Province",
        [""] + list(data['namakp'].unique()),
        index=0,
        format_func=lambda x: "Select province..." if x == "" else x
    )
    product = st.selectbox(
        "Name of Product",
        [""] + list(data['namaproduk'].unique()),
        index=0,
        format_func=lambda x: "Select product..." if x == "" else x
    )
    agent = st.selectbox(
        "Agent Partner",
        [""] + list(data['mitraagen'].unique()),
        index=0,
        format_func=lambda x: "Select agent..." if x == "" else x
    )
    subscription_length = st.slider(
        "Long Subscription",
        1, 12, 3
    )
    num_customers = st.number_input(
        "Number of Customers",
        min_value=1,
        value=1
    )

    # Define the prediction function
    def predict_total_revenue(year, province, product, agent, subscription_length, actual_data, predicted_data, actual_data_2023, num_customers):
        # Filter actual data for the selected province
        actual_revenue_province = actual_data.loc[actual_data['namakp'] == province]

        # Filter actual data for the selected product
        actual_revenue_product = actual_revenue_province.loc[actual_revenue_province['namaproduk'] == product]

        # Filter actual data for the selected agent
        actual_revenue_agent = actual_revenue_product.loc[actual_revenue_product['mitraagen'] == agent]

        # Calculate the average revenue per month for the filtered data
        average_revenue_per_month = actual_revenue_agent['totalharga'].mean() / actual_revenue_agent['lamaberlangganan'].mean()

        # Get the total predicted revenue for the selected year and province
        total_predicted_revenue = predicted_data.loc[province, str(year)]

        # Get the total actual revenue for the base year (2023)
        total_actual_revenue = actual_data_2023.loc[province, '2023']

        # Calculate the scaling factor based on the ratio of total predicted revenue to total actual revenue
        scaling_factor = total_predicted_revenue / total_actual_revenue

        # Scale the average revenue per month
        scaled_average_revenue_per_month = average_revenue_per_month * scaling_factor

        # Calculate the predicted revenue per customer based on the selected subscription length
        predicted_revenue_per_customer = scaled_average_revenue_per_month * subscription_length

        # Calculate the total predicted revenue based on the number of customers
        total_predicted_revenue = predicted_revenue_per_customer * num_customers

        # Penanganan untuk data yang hilang
        actual_revenue_agent = actual_revenue_agent.dropna(subset=['totalharga', 'lamaberlangganan'])

        # Menghindari pembagian dengan nol
        mean_subscription_length = actual_revenue_agent['lamaberlangganan'].mean()
        average_revenue_per_month = actual_revenue_agent['totalharga'].mean() / mean_subscription_length if mean_subscription_length != 0 else 0
        predicted_revenue_per_customer = average_revenue_per_month * subscription_length

        return total_predicted_revenue

    if st.button("Predict Revenue"):
        missing_options = [
            "prediction year" if prediction_year == "" else None,
            "province" if province == "" else None,
            "product" if product == "" else None,
            "agent partner" if agent == "" else None,
        ]
        missing_options = [x for x in missing_options if x is not None]

        if missing_options:
            st.warning(f"Please select the following options before predicting: {', '.join(missing_options)}")
        else:
            # Calculate predicted revenue
            predicted_total_revenue = predict_total_revenue(prediction_year, province, product, agent, subscription_length, data, df_pred, df_actual_2023, num_customers)

            # Display the predicted revenue
            st.metric(label="Total Revenue Prediction", value=f"Rp {predicted_total_revenue:,.2f}")

            # Summary and Analysis
            st.subheader("Summary and Analysis")

            # Comparison with Average Revenue
            all_product_avg_revenue = data['totalharga'].mean()
            all_province_avg_revenue = data.groupby('namakp')['totalharga'].mean()[province]
            all_agent_avg_revenue = data.groupby('mitraagen')['totalharga'].mean()[agent]

            product_comparison = ((predicted_total_revenue - all_product_avg_revenue) / all_product_avg_revenue) * 100
            province_comparison = ((predicted_total_revenue - all_province_avg_revenue) / all_province_avg_revenue) * 100
            agent_comparison = ((predicted_total_revenue - all_agent_avg_revenue) / all_agent_avg_revenue) * 100

            st.write(f"**Analysis for {product} in {province} sold by {agent} in {prediction_year}:**")

            if product_comparison > 0:
                st.write(f"- **Product Performance:** {product} is projected to outperform the average product by {product_comparison:.2f}%. This indicates strong demand and potential for further growth. Consider expanding marketing efforts or exploring opportunities for upselling and cross-selling.")
            else:
                st.write(f"- **Product Performance:** {product} is projected to underperform the average product by {abs(product_comparison):.2f}%. Investigate potential reasons for lower demand, such as market saturation, pricing issues, or competition. Consider adjusting marketing strategies or product offerings to improve performance.")

            if province_comparison > 0:
                st.write(f"- **Regional Performance:** {province} is expected to exceed the average revenue for the region by {province_comparison:.2f}%. This suggests a strong market presence in this area. Continue focusing on this region and consider allocating additional resources to capitalize on the growth potential.")
            else:
                st.write(f"- **Regional Performance:** {province} is projected to underperform compared to the regional average by {abs(province_comparison):.2f}%. Analyze market conditions and identify factors hindering growth in this region. Consider targeted marketing campaigns or partnerships to boost sales.")

            if agent_comparison > 0:
                st.write(f"- **Agent Performance:** {agent} is predicted to generate {agent_comparison:.2f}% more revenue than the average agent. This demonstrates their effectiveness in sales and customer acquisition. Recognize and reward their performance, and consider sharing their best practices with other agents.")
            else:
                st.write(f"- **Agent Performance:** {agent} is projected to generate {abs(agent_comparison):.2f}% less revenue than the average agent. Assess their sales strategies and identify areas for improvement. Provide additional training or support to help them reach their full potential.")
