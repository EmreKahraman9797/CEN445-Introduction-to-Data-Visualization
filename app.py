import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go





st.set_page_config(
    page_title="Netflix Data Visualization Dashboard",
    layout="wide"
)








@st.cache_data
def load_data():
    try:
        df = pd.read_csv("netflix_titles.csv")
    except FileNotFoundError:
        return None

    #basic cleaning
    df = df.copy()
    #parsing dates
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
        df["year_added"] = df["date_added"].dt.year
    else:
        df["year_added"] = pd.NA

    #release year to numeric
    if "release_year" in df.columns:
        df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

    #handle duration: "90 min" or "2 Seasons"
    if "duration" in df.columns:
        duration_split = df["duration"].fillna("").str.extract(r"(\d+)\s*(\w+)?")
        df["duration_int"] = pd.to_numeric(duration_split[0], errors="coerce")
        df["duration_unit"] = duration_split[1].fillna("")
    else:
        df["duration_int"] = pd.NA
        df["duration_unit"] = ""

    #main genre: first item from listed_in
    if "listed_in" in df.columns:
        df["main_genre"] = df["listed_in"].fillna("").str.split(",").str[0].str.strip()
    else:
        df["main_genre"] = ""

    #primary country: first country
    if "country" in df.columns:
        df["primary_country"] = df["country"].fillna("").str.split(",").str[0].str.strip()
    else:
        df["primary_country"] = ""

    return df

df = load_data()












st.title("Netflix Data Visualization Dashboard")

if df is None:
    st.error(
        "Dataset not found. Please download `netflix_titles.csv` from Kaggle"
    )
    st.stop()

st.markdown(
    """
This interactive dashboard explores the **Netflix Movies and TV Shows** dataset
using multiple visualization techniques and interactive controls.
"""
)



# ----------------------- Sidebar Filters ----------------------------

st.sidebar.header("Filters")

type_options = sorted(df["type"].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "Content type",
    options=type_options,
    default=type_options,
)

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
year_range = st.sidebar.slider(
    "Release year range",
    min_value=min_year,
    max_value=max_year,
    value=(2000, max_year),
    step=1,
)

country_options = sorted(
    c for c in df["primary_country"].dropna().unique().tolist() if c
)
selected_countries = st.sidebar.multiselect(
    "Primary country (optional)",
    options=country_options,
    default=[]
)

rating_options = sorted(df["rating"].dropna().unique().tolist())
selected_ratings = st.sidebar.multiselect(
    "Rating (optional)",
    options=rating_options,
    default=[]
)

genre_options = sorted(
    g for g in df["main_genre"].dropna().unique().tolist() if g
)
selected_genres = st.sidebar.multiselect(
    "Main genre (optional)",
    options=genre_options,
    default=[]
)

title_search = st.sidebar.text_input("Title contains (optional)", value="")

# Apply filters
mask = df["type"].isin(selected_types) & df["release_year"].between(
    year_range[0], year_range[1]
)

if selected_countries:
    mask &= df["primary_country"].isin(selected_countries)

if selected_ratings:
    mask &= df["rating"].isin(selected_ratings)

if selected_genres:
    mask &= df["main_genre"].isin(selected_genres)

if title_search:
    mask &= df["title"].str.contains(title_search, case=False, na=False)

filtered = df[mask]

st.markdown(
    f"**Filtered titles:** {len(filtered)} "
    f"(from total {len(df)} entries in the dataset)."
)



# ----------------------- KPI Cards ----------------------------------

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric("Total Titles", len(filtered))

with col_kpi2:
    movies_count = (filtered["type"] == "Movie").sum()
    st.metric("Movies", int(movies_count))

with col_kpi3:
    shows_count = (filtered["type"] == "TV Show").sum()
    st.metric("TV Shows", int(shows_count))

with col_kpi4:
    unique_countries = filtered["primary_country"].replace("", pd.NA).dropna().nunique()
    st.metric("Countries Represented", int(unique_countries))

st.markdown("---")













# ---------------------- 1)Catalog Growth-Line Chart -------------------
st.subheader("1.Catalog Growth-Line Chart")

if filtered["year_added"].notna().any():
    growth = (
        filtered.dropna(subset=["year_added"])
        .groupby("year_added")["show_id"]
        .count()
        .reset_index()
        .sort_values("year_added")
    )
    if not growth.empty:
        fig_growth = px.line(
            growth,
            x="year_added",
            y="show_id",
            markers=True,
            title="How fast is Netflix's library growing?",
        )
        fig_growth.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_growth, use_container_width=True)
    else:
        st.info("No data available for `year_added` with current filters.")
else:
    st.info("`date_added` information is missing for this dataset.")

st.markdown("---")
#-------------------------------------------------------------------------









