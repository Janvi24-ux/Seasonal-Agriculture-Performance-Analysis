import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Seasonal Agriculture Performance Analysis",
    page_icon="🌾",
    layout="wide"
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    file_path = "data/seasonal_agriculture_performance_dataset.csv"
    df = pd.read_csv(file_path)

    # Fill missing numerical values with median
    numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns

    for column in numerical_columns:
        df[column] = df[column].fillna(df[column].median())

    # Fill missing categorical values with mode
    categorical_columns = df.select_dtypes(include=["object"]).columns

    for column in categorical_columns:
        if df[column].isnull().any():
            df[column] = df[column].fillna(df[column].mode()[0])

    return df


df = load_data()

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🌾 Seasonal Agriculture Performance Analysis")

st.markdown(
    """
    This interactive dashboard analyzes agricultural performance across
    different seasons, crops, regions, environmental conditions,
    resource usage and economic outcomes.
    """
)

st.divider()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("🔎 Filters")

# Season filter
seasons = ["All"] + sorted(df["Season"].unique().tolist())
selected_season = st.sidebar.selectbox(
    "Select Season",
    seasons
)

# Crop filter
crops = ["All"] + sorted(df["Crop"].unique().tolist())
selected_crop = st.sidebar.selectbox(
    "Select Crop",
    crops
)

# State filter
states = ["All"] + sorted(df["State"].unique().tolist())
selected_state = st.sidebar.selectbox(
    "Select State",
    states
)

# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df.copy()

if selected_season != "All":
    filtered_df = filtered_df[
        filtered_df["Season"] == selected_season
    ]

if selected_crop != "All":
    filtered_df = filtered_df[
        filtered_df["Crop"] == selected_crop
    ]

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["State"] == selected_state
    ]

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Farms",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Average Yield",
        f"{filtered_df['Yield_Tonnes_Ha'].mean():.2f} t/ha"
    )

with col3:
    st.metric(
        "Average Revenue",
        f"₹{filtered_df['Revenue_INR'].mean():,.0f}"
    )

with col4:
    st.metric(
        "Average Profit",
        f"₹{filtered_df['Profit_INR'].mean():,.0f}"
    )

st.divider()

# ---------------------------------------------------------
# SEASONAL PERFORMANCE
# ---------------------------------------------------------

st.header("🌱 Seasonal Agricultural Performance")

season_summary = (
    filtered_df
    .groupby("Season")
    .agg(
        Average_Yield=("Yield_Tonnes_Ha", "mean"),
        Production=("Production_Tonnes", "sum"),
        Revenue=("Revenue_INR", "sum"),
        Profit=("Profit_INR", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

# Yield by Season
with col1:
    st.subheader("Yield by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=season_summary,
        x="Season",
        y="Average_Yield",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Average Yield (Tonnes/Ha)")
    ax.set_title("Average Yield Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# Production by Season
with col2:
    st.subheader("Production by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=season_summary,
        x="Season",
        y="Production",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Production (Tonnes)")
    ax.set_title("Total Production Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# ---------------------------------------------------------
# ECONOMIC PERFORMANCE
# ---------------------------------------------------------

st.header("💰 Economic Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=season_summary,
        x="Season",
        y="Revenue",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Revenue (INR)")
    ax.set_title("Revenue Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Profit by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=season_summary,
        x="Season",
        y="Profit",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Profit (INR)")
    ax.set_title("Profit Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# ---------------------------------------------------------
# ENVIRONMENTAL CONDITIONS
# ---------------------------------------------------------

st.header("🌦️ Environmental Conditions")

environment_summary = (
    filtered_df
    .groupby("Season")
    .agg(
        Rainfall=("Rainfall_mm", "mean"),
        Temperature=("Avg_Temperature_C", "mean"),
        Soil_Moisture=("Soil_Moisture_pct", "mean"),
        Humidity=("Humidity_pct", "mean")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Rainfall by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=environment_summary,
        x="Season",
        y="Rainfall",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title("Average Rainfall Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Average Temperature by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=environment_summary,
        x="Season",
        y="Temperature",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Average Temperature Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# ---------------------------------------------------------
# WATER USAGE
# ---------------------------------------------------------

st.header("💧 Water Resource Analysis")

water_summary = (
    filtered_df
    .groupby("Season")
    .agg(
        Water_Used=("Water_Used_m3", "mean"),
        Water_Efficiency=("Water_Efficiency_t_per_1000m3", "mean")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Water Usage by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=water_summary,
        x="Season",
        y="Water_Used",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Water Used (m³)")
    ax.set_title("Average Water Usage Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Water Efficiency by Season")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=water_summary,
        x="Season",
        y="Water_Efficiency",
        ax=ax
    )

    ax.set_xlabel("Season")
    ax.set_ylabel("Tonnes / 1000 m³")
    ax.set_title("Average Water Efficiency Across Seasons")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# ---------------------------------------------------------
# DISEASE / PEST RISK
# ---------------------------------------------------------

st.header("🐛 Disease and Pest Risk")

risk_summary = (
    filtered_df
    .groupby("Season")["Disease_Pest_Risk_pct"]
    .mean()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=risk_summary,
    x="Season",
    y="Disease_Pest_Risk_pct",
    ax=ax
)

ax.set_xlabel("Season")
ax.set_ylabel("Disease/Pest Risk (%)")
ax.set_title("Average Disease and Pest Risk by Season")

plt.xticks(rotation=20)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------
# CROP × SEASON HEATMAP
# ---------------------------------------------------------

st.header("🔥 Crop and Season Analysis")

crop_season = filtered_df.pivot_table(
    values="Yield_Tonnes_Ha",
    index="Crop",
    columns="Season",
    aggfunc="mean"
)

fig, ax = plt.subplots(figsize=(12, 7))

sns.heatmap(
    crop_season,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu",
    ax=ax
)

ax.set_title("Average Yield by Crop and Season")
ax.set_xlabel("Season")
ax.set_ylabel("Crop")

plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------
# ENVIRONMENT VS YIELD
# ---------------------------------------------------------

st.header("📈 Environmental Conditions vs Yield")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rainfall vs Yield")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        data=filtered_df,
        x="Rainfall_mm",
        y="Yield_Tonnes_Ha",
        hue="Season",
        ax=ax
    )

    ax.set_xlabel("Rainfall (mm)")
    ax.set_ylabel("Yield (Tonnes/Ha)")
    ax.set_title("Rainfall vs Agricultural Yield")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Temperature vs Yield")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        data=filtered_df,
        x="Avg_Temperature_C",
        y="Yield_Tonnes_Ha",
        hue="Season",
        ax=ax
    )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Yield (Tonnes/Ha)")
    ax.set_title("Temperature vs Agricultural Yield")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# ---------------------------------------------------------
# SEASON DISTRIBUTION
# ---------------------------------------------------------

st.header("📊 Season Distribution")

season_counts = filtered_df["Season"].value_counts().reset_index()
season_counts.columns = ["Season", "Number_of_Farms"]

fig, ax = plt.subplots(figsize=(9, 5))

sns.barplot(
    data=season_counts,
    x="Season",
    y="Number_of_Farms",
    ax=ax
)

ax.set_xlabel("Season")
ax.set_ylabel("Number of Farms")
ax.set_title("Number of Farms by Season")

plt.xticks(rotation=20)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------

st.header("📋 Dataset Preview")

st.write(
    f"Showing {len(filtered_df):,} records based on the selected filters."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Seasonal Agriculture Performance Analysis | VOIS AICTE Batch 1 2026–2027"
)