# Netflix Data Visualization Dashboard
# CEN445 - Introduction to Data Visualization

## Project Overview
This interactive dashboard was developed as a group assignment to explore and visualize the Netflix dataset. Using Python as Streamlit, we built a responsive web
applicaiton that reverse -engineers Netflix's content strategy. The dashboard features 9 distinct visualizatin techniques to uncover trends in content duration,
regional preferences, and maturity ratings.

## Files in Repository
* app.py: The main source code of application.
* netflix_titlesdata.csv: The dataset that is used for analysis.
* README.md: Documentation and setup guide.

## Dataset Details
- Source: Kaggle -> Netflix Movies and TV Shows
- Size: ~8,800 rows and 12 columns.
- Key Attributes: Type, Title, Director, Cast, Country, Date Added, Release Year, Rating, Duration, Listed in.

## Contributions & Roles
The development of this dashboard was a collaborative effort. Specific responsibilities were divided as follows:

### Emre Kahraman:
- Core Responsibility: Data Preprocessing & Foundation
- Implemented the load_data function, handling null values, and parsing dates/durations.
- Standardized the genre columns (e.g., cleaning "Movies" labels).

Visualizations:
1. Graph 1 (Line Chart): Catalog Growth Over Years.
2. Graph 2 (Choropleth Map): Global Content Distribution.
3. Graph 3 (Treemap): Genre Composition by Type.

### Asusena Ela Öztürk:
- Core Responsibility: UI/UX Design & Interactivity
- Designed the sidebar layout, global filters (Year/Country/Genre), and dashboard responsiveness.
- Managed the "Advanced Visualizations" implementation using Plotly Graph Objects.

Visualizations:
1. Graph 4 (Histogram): Movie Runtime Analysis.
2. Graph 5 (Sunburst Chart): Regional Genre Preferences.
3. Graph 6 (Parallel Coordinates): Evolution of Movie Lengths (2010-2021).

### Orhan Karaman:
- Core Responsibility: Documentation & Analytical Flow
- Also authored the project report and README file.
- Refined graph titles and "Tool Tip" captions for better user understanding.

Visualizations:
1. Graph 7 (Bar Chart): Top Dominant Genres.
2. Graph 8 (Sankey Diagram): Content Maturity Flow.
3. Graph 9 (Heatmap): Rating Intensity by Format.

## Installation & Setup
To run this dashboard locally, follow these steps:

### Clone the repository:
- git clone https://github.com/EmreKahraman9797/CEN445-Introduction-to-Data-Visualization.git
- cd CEN445-Introduction-to-Data-Visualization


### Install required libraries:
#### Ensure you have Python installed, then run:
```pip install streamlit pandas plotly```

#### Run the App:
```python -m streamlit run app.py```
