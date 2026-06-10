import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="APL Logistics Dashboard",
    page_icon="📦",
    layout="wide"
)
st.markdown("""
### 🚚 Supply Chain Intelligence Platform

Analyze delivery performance, delay risks,
regional bottlenecks and shipping efficiency.
""")


@st.cache_data
def load_data():
    return pd.read_csv(
        "data/APL_Logistics.csv",
        encoding="latin1"
    )

df = load_data()


df["Delivery Gap"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

def classify_delivery(x):
    if x > 0:
        return "Delayed"
    elif x == 0:
        return "On-Time"
    else:
        return "Early"

df["Delivery Category"] = df["Delivery Gap"].apply(
    classify_delivery
)



st.sidebar.header("Dashboard Filters")

shipping_mode = st.sidebar.multiselect(
    "Shipping Mode",
    options=df["Shipping Mode"].dropna().unique(),
    default=df["Shipping Mode"].dropna().unique()
)

market = st.sidebar.multiselect(
    "Market",
    options=df["Market"].dropna().unique(),
    default=df["Market"].dropna().unique()
)

customer_segment = st.sidebar.multiselect(
    "Customer Segment",
    options=df["Customer Segment"].dropna().unique(),
    default=df["Customer Segment"].dropna().unique()
)

filtered_df = df[
    (df["Shipping Mode"].isin(shipping_mode))
    & (df["Market"].isin(market))
    & (df["Customer Segment"].isin(customer_segment))
]



st.title("📦 APL Logistics Intelligence Dashboard")

st.markdown(
    """
    ### Delivery Performance, Delay Risk &
    Logistics Efficiency Analysis
    """
)



total_orders = len(filtered_df)

on_time_orders = len(
    filtered_df[
        filtered_df["Delivery Category"] == "On-Time"
    ]
)

on_time_rate = (
    on_time_orders / total_orders * 100
    if total_orders > 0
    else 0
)

avg_delay = filtered_df["Delivery Gap"].mean()

late_risk = (
    filtered_df["Late_delivery_risk"].mean() * 100
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 Total Orders",
        f"{total_orders:,}"
    )

with col2:
    st.metric(
        "✅ On-Time Rate",
        f"{on_time_rate:.2f}%"
    )

with col3:
    st.metric(
        "⏳ Avg Delay",
        f"{avg_delay:.2f} Days"
    )

with col4:
    st.metric(
        "⚠️ Late Risk",
        f"{late_risk:.2f}%"
    )

st.divider()



col1, col2 = st.columns(2)

with col1:

    delivery_counts = (
        filtered_df["Delivery Category"]
        .value_counts()
        .reset_index()
    )

    delivery_counts.columns = [
        "Status",
        "Count"
    ]

    fig1 = px.pie(
        delivery_counts,
        names="Status",
        values="Count",
        title="Delivery Status Distribution",
        hole=0.4
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    fig2 = px.histogram(
        filtered_df,
        x="Delivery Gap",
        nbins=30,
        title="Delivery Gap Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )



st.subheader("🚚 Shipping Mode Analysis")

shipping_analysis = (
    filtered_df
    .groupby("Shipping Mode")["Delivery Gap"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    shipping_analysis,
    x="Shipping Mode",
    y="Delivery Gap",
    color="Delivery Gap",
    text_auto=True,
    title="Average Delay by Shipping Mode"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)



st.subheader("🌍 Regional Delay Analysis")

region_analysis = (
    filtered_df
    .groupby("Order Region")["Delivery Gap"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    region_analysis,
    x="Order Region",
    y="Delivery Gap",
    color="Delivery Gap",
    text_auto=True,
    title="Regional Delay Index"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)



st.subheader("👥 Customer Segment Analysis")

segment_analysis = (
    filtered_df
    .groupby("Customer Segment")["Delivery Gap"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    segment_analysis,
    x="Customer Segment",
    y="Delivery Gap",
    color="Delivery Gap",
    text_auto=True,
    title="Average Delay by Customer Segment"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)



st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head(50))


csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="APL_Logistics_Filtered.csv",
    mime="text/csv"
)
st.markdown("---")
st.subheader("🌍 Global Logistics Performance Map")

country_analysis = (
    filtered_df.groupby("Order Country")["Delivery Gap"]
    .mean()
    .reset_index()
)

fig6 = px.choropleth(
    country_analysis,
    locations="Order Country",
    locationmode="country names",
    color="Delivery Gap",
    hover_name="Order Country",
    color_continuous_scale="RdYlGn_r",
    title="Average Delivery Delay by Country"
)

st.plotly_chart(fig6, use_container_width=True)
st.markdown("---")
st.subheader("📦 Top Delayed Product Categories")

category_analysis = (
    filtered_df.groupby("Category Name")["Delivery Gap"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig7 = px.bar(
    category_analysis,
    x="Delivery Gap",
    y="Category Name",
    orientation="h",
    color="Delivery Gap",
    title="Top 10 Delayed Categories"
)

st.plotly_chart(fig7, use_container_width=True)
st.markdown("---")
st.subheader("💰 Sales vs Profit Analysis")

fig8 = px.scatter(
    filtered_df,
    x="Sales",
    y="Order Profit Per Order",
    color="Customer Segment",
    title="Sales vs Profit Relationship"
)

st.plotly_chart(fig8, use_container_width=True)
st.markdown("---")
st.subheader("📈 Market-wise Delay Risk")

market_analysis = (
    filtered_df.groupby("Market")["Late_delivery_risk"]
    .mean()
    .reset_index()
)

market_analysis["Late_delivery_risk"] *= 100

fig9 = px.bar(
    market_analysis,
    x="Market",
    y="Late_delivery_risk",
    color="Late_delivery_risk",
    text_auto=True,
    title="Late Delivery Risk by Market (%)"
)

st.plotly_chart(fig9, use_container_width=True)
st.markdown("---")
st.subheader("🎯 Executive Summary")

st.success(f"""
Total Orders: {total_orders:,}

On-Time Delivery Rate: {on_time_rate:.2f}%

Average Delay: {avg_delay:.2f} Days

Late Delivery Risk: {late_risk:.2f}%

This dashboard helps identify logistics bottlenecks,
shipping inefficiencies, and regional delay risks.
""")
st.write("NEW VERSION LOADED 🚀")
