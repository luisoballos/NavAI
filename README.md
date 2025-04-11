# Madrid Accessibility Evaluation Dashboard (2020-2024)

## Project objective
This project aims to analyze and visualize improvements in accessibility infrastructure (ramps, sidewalks, pedestrian crossings, etc.) for people with disabilities in Madrid between 2020 and 2024. The dashboard provides insights into changes across districts and years, helping stakeholders assess progress and identify areas for further improvement.

## Dashboard features
- **Year and district selector**: Filter data by specific years and districts.
- **KPI progress metrics**: Track key performance indicators for accessibility improvements.
- **Interactive map**: Visualize the geographical distribution of accessibility improvements.
- **Comparative analysis**: Compare changes in accessibility between selected years.

## Project structure

The project is structured as follows:

```
├── data/                  # Raw and processed data files
│   ├── raw/               # Original datasets (e.g., shapefiles)
│   └── processed/         # Cleaned and transformed datasets
├── notebooks/             # Jupyter Notebooks for analysis and testing
├── img/                   # Images and visualizations for documentation
├── dashboards/            # Power BI (.pbix) or Tableau files
├── src/                   # Python scripts for ETL, statistics, etc.
│   ├── etl/               # ETL-related files
│   │   ├── etl_images/    # Supporting files for ETL processes
│   │   └── etl_dataset.py # ETL files
│   ├── eda.py             # Exploratory Data Analysis files
│   └── stats.py           # Statistical analysis files
├── requirements.txt       # Project dependencies
├── .gitignore             # Files and directories to ignore in version control
└── README.md              # Project documentation
```

## ETL process

### 1. Data sources
The project uses shapefiles provided by the *Ayuntamiento de Madrid* that contain accessibility data.

### 2. Extraction
The raw datasets are loaded using `geopandas` for geospatial analysis:

```python
import geopandas as gpd

# Load raw datasets
gdf_1 = gpd.read_file({file_path})
gdf_2 = gpd.read_file({file_path})
gdf_3 = gpd.read_file({file_path})

gdf = gpd.GeoDataFrame(
    pd.concat([gdf_1, gdf_2, gdf_3], ignore_index=True),
    geometry='geometry'
)
```

### 3. Transformation
The data is cleaned, transformed, and stored in the `data/processed/` directory for further analysis.

### 4. Loading
Processed data is used to generate visualizations and populate the dashboard.

## Data visualization
The dashboard includes:
- **Interactive maps**: Highlighting accessibility improvements by location.
- **KPIs**: Metrics to track progress over time.
- **Comparative charts**: Year-over-year analysis of accessibility improvements.

## Requirements
To run the project, install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Getting started
1. Clone the repository:
   ```bash
   git clone https://github.com/luisoballos/NavAI
   ```
2. Navigate to the project directory:
   ```bash
   cd madrid-accessibility-dashboard
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the ETL scripts in the `src/etl/` directory to process the data.

## Repository contents
- **`data/`**: Contains raw and processed data files.
- **`notebooks/`**: Jupyter Notebooks for exploratory analysis and testing.
- **`src/`**: Python scripts for ETL, EDA, and statistical analysis.
- **`dashboards/`**: Power BI or Tableau files for visualization.
- **`img/`**: Images used in documentation and presentations.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.
---