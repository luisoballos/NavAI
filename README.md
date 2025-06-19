# NavAI: Accessible Urban Navigation for Madrid

NavAI is an innovative application designed to enhance urban accessibility for people with disabilities in Madrid. By leveraging advanced AI (Computer Vision) and comprehensive geospatial data, NavAI provides real-time, accessible route navigation, addressing the critical need for inclusive urban mobility. Our core objective is to empower individuals with disabilities by offering reliable, detailed, and personalized navigation experiences, and to provide urban planners with actionable insights for infrastructure improvement.

## Key Features

NavAI offers a unique set of functionalities for both end-users and urban development stakeholders:

* **Accessible Route Generation**:
    * Utilizes Google's Routes API for base routing.
    * Integrates custom accessibility data (sidewalk width, buzzer locations, construction zones) to create optimal accessible paths.
    * Real-time crosswalk detection via AI (Google Gemini API): Analyzes Google Street View images along the route to identify and confirm the presence of crosswalks, enhancing route accuracy.
    * Dynamic accessibility scoring: Each generated route receives an accessibility score (0-100) based on critical criteria:
        * Percentage of crosswalks with acoustic buzzers: Reflects auditory guidance availability.
        * Average sidewalk width: Ensures pathways meet accessibility standards (e.g., minimum 1.5 meters).

* **Interactive Map Visualization (React-Leaflet)**:
    * Displays the generated accessible route.
    * Highlights key accessibility features: **buzzers, sidewalk widths, construction zones, and detected crosswalks**.
    * Shows the route's start and end markers.
    * **Accessibility Legend**: Provides a clear visual guide to route segment accessibility (Fully Accessible, Partially Accessible, Poorly Accessible, Unknown).

* **User-Centric Frontend (React & Vite)**:
    * Intuitive User Interface: Allows users to set origin, destination, and select specific impairment types (e.g., wheelchair, visual impairment).
    * Seamless User Flow: Includes dedicated `Home`, `Loading`, and `Navigation` (map view) pages for a smooth user experience.
    * Dynamic Data Display: Presents the calculated accessibility score directly within the navigation interface.

* **Urban Planning Insights (Backend Analytics)**:
    * Analyzes and visualizes improvements in accessibility infrastructure across Madrid.
    * Year and district selector: Filter data for targeted analysis.
    * KPI progress metrics: Track key performance indicators for accessibility improvements over time.
    * Comparative analysis: Compare changes in accessibility between selected years.
    * Interactive maps: Visualize the geographical distribution of accessibility improvements based on historical data.

## Project Structure

The project is structured into distinct Python (backend/data processing) and React (frontend) components. The frontend interacts with the backend via API calls.

```
├── data/                        # Geospatial data files from Ayuntamiento de Madrid
│   ├── processed/               # Cleaned and standardized GeoJSON data
├── public/                      # Static assets for the React app, including generated HTML map and JSON score
│   └── (icons for React app)    # blind-icon.png and wheelchair-icon.png
├── src/                         # Source code for both Python backend and React frontend
│   ├── etl/                     # Python scripts for ETL processes (data fetching, cleaning, transformation)
│   │   ├── get_route.py         # Fetches route polyline from Google Routes API
│   │   ├── get_images.py        # Fetches Street View images
│   │   └── etl_dataset.py       # Processes buzzers, constructions, and sidewalks datasets
│   │   └── (other ETL related files)
│   ├── image_analysis.py        # Python script for AI-powered image analysis (crosswalk detection)
and map/score output
│   ├── components/             # Reusable React UI components (e.g., Navbar, Footer, MapLegend)
│   ├── pages/                  # React app pages (e.g., Home, Loading, Navegation, ErrorPage, Layout)
│   ├── routes.jsx              # React Router setup for navigation
│   ├── index.css               # Global CSS styles
│   └── main.jsx                # React app entry point
├── API_KEY.txt             # Placeholder for API keys
├── requirements.txt            # Python project dependencies
├── package.json                # Node.js/Vite project dependencies
├── .gitignore                  # Files and directories to ignore in version control
└── README.md                   # Project documentation
```

## Backend Overview
The backend, built with Flask, serves as the brain of NavAI. It handles:

* **Route calculation:** Integrates with Google Routes API.
* **Geospatial data processing:** Intersects the calculated route with local accessibility datasets (sidewalks, buzzers, constructions) using `geopandas`.
* **Street View analysis:** Fetches Street View images and sends them to Gemini API for crosswalk detection.
* **Accessibility evaluation:** Computes the overall accessibility score for the route.
* **API exposure:** Provides a RESTful API (`/api/route_analysis`) for the frontend to request route information and accessibility analysis.

## Frontend Overview
The frontend, built with **React** and bundled with Vite, provides the interactive user experience. It handles:

* **User input:** Captures origin, destination, and impairment type.
* **API communication:** Sends route requests to the Flask backend.
* **Map visualization:** Displays the route and accessibility data using `react-leaflet`.
* **Dynamic UI:** Manages loading states, displays the accessibility score, and provides a smooth navigation flow.

## Requirements
To run the project, ensure you have both **Python (3.8+)** and **Node.js (14+)** installed.

### API Keys
You will need **one Google API Key** enabled for:
* Routes API
* Maps Static API
* Street View Static API
* Cloud Text-to-Speech API (when Further Work is implemented)
* Generative Language API

**Configuration:** Create a file named `API_KEY.txt` in the root directory of your project (same level as `README.md`). Paste your single Google API Key into the first line of this file. **Important:** `API_KEY.txt` is already included in `.gitignore` for security reasons.

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
git clone [https://github.com/luisoballos/NavAI](https://github.com/luisoballos/NavAI)
cd NavAI
```

2. Create API_KEY.txt and paste your Google API Key there:
```bash
touch API_KEY.txt
```

3. Install dependencies:
```bash
pip install -r requirements.txt
npm install
```

4. Run the Python Backend (Flask API):
Open a new terminal and navigate to the project root:

```bash
flask --app src/app run --debug
```

This will start the Flask development server, typically on `http://127.0.0.1:5000` or `http://localhost:5000`. The --debug flag is useful for development as it provides auto-reloading and debugging information.

5. Run the React Frontend (in another separate terminal):
   This will start the Vite development server.
```bash
npm run dev
```

6. Access the application:
   Open your web browser and navigate to the URL provided by Vite (e.g., `http://localhost:5173`). Use the navigation links within the app to access the map page.

## Further Work & Future Vision
NavAI is continuously evolving. My long-term vision includes:

- **Enhanced data integration**: Incorporating more granular accessibility data points (e.g., curb cuts, ramps, surface textures, real-time obstacles).
- **Indoor navigation**: Extending accessibility guidance to public buildings and transportation hubs.
- **Predictive accessibility**: Utilizing machine learning to predict future accessibility challenges based on urban development plans.
- **Community contributions**: Implementing features for users to report and update accessibility information.
- **Expanded geographical coverage**: Scaling the solution to other cities globally, adapting to local accessibility standards and data sources.
- **Deep learning models**: Developing custom deep learning models for even more precise object detection and environmental analysis.

## Contributing
Contributions are highly encouraged! Please feel free to fork the repository, open issues, and submit pull requests with your improvements and features.