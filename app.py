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







