import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Methane Emissions Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("clean_methane.csv")

# Clean country names
df["Country Name"] = df["Country Name"].astype(str).str.strip()

# Remove non-country / grouped entries
df = df[~df["Country Name"].str.contains(
    "Euro|World|OECD|Union|income|countries|area|IBRD|IDA|Africa|Asia|Europe",
    case=False,
    na=False
)]

# Dashboard title
st.title("🌍 Global Methane Emissions Dashboard")
st.markdown("### Data-driven insights on methane emissions across countries")

st.write(
    "This dashboard analyses methane emissions by country using World Bank data. "
    "Users can explore country-level trends and compare the highest methane-emitting countries."
)

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Countries", df["Country Name"].nunique())
col2.metric("Highest Emission", round(df["Methane"].max(), 2))
col3.metric("Lowest Emission", round(df["Methane"].min(), 2))

# Sidebar filters
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["Country Name"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

# Filter data
filtered = df[
    (df["Country Name"] == country) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Line chart
st.subheader(f"📈 Methane Emissions Trend - {country}")

fig_line = px.line(
    filtered,
    x="Year",
    y="Methane",
    markers=True,
    title=f"Methane Emissions Trend in {country}",
    labels={"Methane": "Methane Emissions", "Year": "Year"}
)

st.plotly_chart(fig_line, use_container_width=True)

# Top 10 chart
st.subheader("🏆 Top 10 Countries by Average Methane Emissions")

top10 = (
    df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
    .groupby("Country Name")["Methane"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_bar = px.bar(
    top10,
    x="Country Name",
    y="Methane",
    text=top10["Methane"].round(1),
    title="Top 10 Countries by Average Methane Emissions",
    labels={"Methane": "Average Methane Emissions", "Country Name": "Country"}
)

fig_bar.update_traces(textposition="outside")
fig_bar.update_layout(xaxis_tickangle=-30)

st.plotly_chart(fig_bar, use_container_width=True)

# Insights
st.markdown("""
### 🔍 Key Insights
- China, United States, and India are among the highest methane-emitting countries.
- Methane emissions vary significantly between countries.
- The dashboard allows users to compare trends across different years and countries.
""")

# Dataset summary instead of dataframe
st.subheader("📊 Dataset Summary")
st.write(f"The cleaned dataset contains **{df.shape[0]} rows** and **{df.shape[1]} columns**.")
st.write(f"The dataset covers **{df['Country Name'].nunique()} countries** from **{df['Year'].min()} to {df['Year'].max()}**.")

# Footer
st.markdown("---")
st.markdown("📌 Data Source: World Bank Open Data")
st.markdown("👨‍💻 Developed for 5DATA004C Data Science Project Lifecycle Coursework")

