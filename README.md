# NavAI: 

NavAI is an innovative application designed to enhance urban accessibility for people with disabilities in Madrid. By leveraging advanced AI (Computer Vision) and comprehensive geospatial data, NavAI provides real-time, accessible route navigation, addressing the critical need for inclusive urban mobility. Our core objective is to empower individuals with disabilities by offering reliable, detailed, and personalized navigation experiences, and to provide urban planners with actionable insights for infrastructure improvement.

## Key Features

NavAI offers a unique set of functionalities for both end-users and urban development stakeholders:

* **Intelligent Accessible Route Generation**:
    * Utilizes Google's Routes API for base routing.
    * **Integrates custom accessibility data** (sidewalk width, buzzer locations, construction zones) to create optimal accessible paths.
    * **NEW:** **Real-time Crosswalk Detection via AI (OpenAI Vision API)**: Analyzes Google Street View images along the route to identify and confirm the presence of crosswalks, enhancing route accuracy.
    * **NEW:** **Dynamic Accessibility Scoring**: Each generated route receives an accessibility score (0-100) based on critical criteria:
        * **Percentage of Crosswalks with Acoustic Buzzers**: Reflects auditory guidance availability.
        * **Average Sidewalk Width**: Ensures pathways meet accessibility standards (e.g., minimum 1.5 meters).

* **Interactive Map Visualization (Folium)**:
    * Displays the generated accessible route.
    * Highlights key accessibility features: **buzzers, sidewalk widths, construction zones, and detected crosswalks**.
    * **NEW:** Shows the user's current location on the map for real-time guidance.

* **User-Centric Frontend (React & Vite)**:
    * **Intuitive User Interface**: Allows users to set origin, destination, and select specific impairment types (e.g., wheelchair, visual impairment).
    * **Seamless User Flow**: Includes dedicated `Home`, `Loading`, and `Navigation` (map view) pages for a smooth user experience.
    * **Dynamic Data Display**: Presents the calculated accessibility score directly within the navigation interface.

* **Urban Planning Insights (Backend Analytics)**:
    * Analyzes and visualizes improvements in accessibility infrastructure across Madrid.
    * **Year and district selector**: Filter data for targeted analysis.
    * **KPI progress metrics**: Track key performance indicators for accessibility improvements over time.
    * **Comparative analysis**: Compare changes in accessibility between selected years.
    * **Interactive maps**: Visualize the geographical distribution of accessibility improvements based on historical data.

## Project Structure

The project is structured into distinct Python (backend/data processing) and React (frontend) components:

```
├── data/                       # Raw and processed geospatial data files
│   ├── processed/              # Cleaned and standardized GeoJSON data
├── public/                     # Static assets for the React app, including generated HTML map and JSON score
│   ├── route_map.html          # Interactive map generated by Python
│   └── accessibility_score.json# Accessibility score calculated by Python
│   └── (icons for React app)   # e.g., wheelchair-icon.svg, blind-icon.svg, settings-icon.svg
├── notebooks/                  # Jupyter Notebooks for exploratory analysis and testing
├── src/                        # Source code for both Python backend and React frontend
│   ├── etl/                    # Python scripts for ETL processes (data fetching, cleaning, transformation)
│   │   ├── get_route.py        # Fetches route polyline from Google Routes API
│   │   ├── get_images.py       # Fetches Street View images
│   │   └── etl_dataset.py      # Processes buzzers, constructions, and sidewalks datasets
│   │   └── (other ETL related files)
│   ├── image_analysis.py       # Python script for AI-powered image analysis (crosswalk detection)
│   ├── plot.py                 # Python script to generate the Folium map HTML
│   ├── main.py                 # Orchestrates the backend logic: route generation, image analysis, accessibility evaluation, and map/score output
│   │
│   ├── components/             # Reusable React UI components (e.g., Navbar, Footer, Navegation - for map display)
│   ├── pages/                  # React app pages (e.g., Home, Loading, ErrorPage, Layout)
│   ├── routes.jsx              # React Router setup for navigation
│   ├── index.css               # Global CSS styles
│   ├── main.jsx                # React app entry point
│   ├── App.jsx                 # Main React application component
│   └── API_KEY.txt             # Placeholder for API keys
├── requirements.txt            # Python project dependencies
├── package.json                # Node.js/Vite project dependencies
├── .gitignore                  # Files and directories to ignore in version control
└── README.md                   # Project documentation
```

## ETL Process

### 1. Data Sources
Utilizes shapefiles from the *Ayuntamiento de Madrid* for accessibility data (buzzers, sidewalks, constructions).

### 2. Google APIs
Integrates Google Routes API for route generation and Google Street View Static API for image fetching.

### 3. Processing
Raw datasets are loaded, cleaned, transformed using `geopandas`, and stored as `.geojson` files in `data/processed/`. Route polylines are decoded using `googlemaps.convert`.

## Street View Image Processing & AI Integration
NavAI uses the Google Street View Static API to fetch high-resolution images along the determined route. These images are then processed using OpenAI Vision API for advanced computer vision tasks, primarily to detect the presence of crosswalks. This analysis directly feeds into our accessibility scoring system, providing granular and real-time insights into pedestrian infrastructure.

## Accesibility evaluation
Our custom `evaluate_accessibility` function determines a route's score (0-100) based on:

The proportion of detected crosswalks that have acoustic buzzers nearby.
The average width of sidewalks along the route, ensuring compliance with accessibility standards (e.g., >= 1.5 meters). This provides a quantifiable metric for route inclusivity.

## Requirements
To run the project, ensure you have both Python and Node.js installed.

### Python dependencies
Install Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Node.js dependencies
```bash
npm install
```

## Getting Started
Follow these steps to run NavAI:
1. Clone the repository:
```bash
git clone https://github.com/luisoballos/NavAI
```
3. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```
4. Prepare your API Keys:
   Ensure your Google API Key and OpenAI API Key are correctly configured (e.g., in `API_KEY.txt` or environment variables as per your setup).

5. Run the Python Backend (in a separate terminal):
   This script will process data, generate the map HTML (`route_map.html`), and the accessibility score JSON (`accessibility_score.json`). You must run this whenever you want to update the map or score.
```bash
python src/main.py
```

6. Run the React Frontend (in another separate terminal):
   This will start the Vite development server.
```bash
npm run dev
```

7. Access the application:
   Open your web browser and navigate to the URL provided by Vite (e.g., `http://localhost:5173`). Use the navigation links within the app to access the map page.

## Further Work & Future Vision
NavAI is continuously evolving. Our long-term vision includes:

- **Enhanced Data Integration**: Incorporating more granular accessibility data points (e.g., curb cuts, ramps, surface textures, real-time obstacles).
- **Indoor Navigation**: Extending accessibility guidance to public buildings and transportation hubs.
- **Predictive Accessibility**: Utilizing machine learning to predict future accessibility challenges based on urban development plans.
- **Community Contributions**: Implementing features for users to report and update accessibility information.
- **Expanded Geographical Coverage**: Scaling the solution to other cities globally, adapting to local accessibility standards and data sources.
- **Deep Learning Models**: Developing custom deep learning models for even more precise object detection and environmental analysis.

## Contributing
Contributions are highly encouraged! Please feel free to fork the repository, open issues, and submit pull requests with your improvements and features.