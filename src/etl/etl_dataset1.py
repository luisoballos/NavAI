import geopandas as gpd
import pandas as pd
import folium

#### Extraction datasets accessibility ####
gdf20 = gpd.read_file("data/raw/Accesibilidad_2020/Accesibilidad.shp")
gdf21 = gpd.read_file("data/raw/Accesibilidad_2021/ACCESIBILIDAD_ACERAS_2021.shp")
gdf24 = gpd.read_file("data/raw/Accesibilidad_2024/ACCESIBILIDAD_ACERAS_2024.shp")

#### Transform ####
gdf20.columns = [i.upper() for i in gdf20.columns]
gdf21.columns = [i.upper() for i in gdf21.columns]
gdf24.columns = [i.upper() for i in gdf24.columns]

column_rename = {
    "CALZADA_M2":"ROAD_AREA",
    "DISTRITO":"DISTRICT",
    "P_P_NUEVOS":"NEW_SIDEWALKS",
    "P_P_RENOVA":"RENEWED_SIDEWALKS",
    "ACERA_M2":"SIDEWALKS_AREA",

    "PASPEA_NUE":"NEW_SIDEWALKS",
    "PASPEA_REN":"RENEWED_SIDEWALKS",
    "SUP_CALZAD":"ROAD_AREA",
    "SUP_ACERA":"SIDEWALKS_AREA",
    "DISTRITO":"DISTRICT",

    "DISTRITOTX":"DISTRICT",
    "SUPCALZADA":"ROAD_AREA",
    "SUPACERA":"SIDEWALKS_AREA",
    "PASOSNUEVO":"NEW_SIDEWALKS",
    "PASOSRENOV":"RENEWED_SIDEWALKS"
}

gdf20 = gdf20.rename(columns=column_rename)
gdf21 = gdf21.rename(columns=column_rename)
gdf24 = gdf24.rename(columns=column_rename)

gdf20 = gdf20[['DISTRICT','ROAD_AREA','SIDEWALKS_AREA','NEW_SIDEWALKS','RENEWED_SIDEWALKS','GEOMETRY']]
gdf21 = gdf21[['DISTRICT','ROAD_AREA','SIDEWALKS_AREA','NEW_SIDEWALKS','RENEWED_SIDEWALKS','GEOMETRY']]
gdf24 = gdf24[['DISTRICT','ROAD_AREA','SIDEWALKS_AREA','NEW_SIDEWALKS','RENEWED_SIDEWALKS','GEOMETRY']]

gdf20['YEAR'] = 2020
gdf21['YEAR'] = 2021
gdf24['YEAR'] = 2024

# Split DISTRICT
gdf20[['DISTRICT']] = gdf20['DISTRICT'].str.extract(r'\d+[\.\s]*(.*)')
gdf21[['DISTRICT']] = gdf21['DISTRICT'].str.extract(r'\d+[\.\s]*(.*)')
gdf24[['DISTRICT']] = gdf24['DISTRICT'].str.extract(r'\d+[\.\s]*(.*)')

# Ensure geometry consistency
for df in [gdf20, gdf21, gdf24]:
    geom_col = [col for col in df.columns if df[col].dtype == 'geometry'][0]
    if geom_col != 'geometry':
        df.rename(columns={geom_col: 'geometry'}, inplace=True)
        df.set_geometry('geometry', inplace=True)
    
    df.set_crs("EPSG:25830", allow_override=True, inplace=True)

# Concatenate
gdf = gpd.GeoDataFrame(
    pd.concat([gdf20, gdf21, gdf24], ignore_index=True),
    geometry='geometry'
)

#Drop NAs
gdf = gdf.dropna()

corrections = {
    'Latina':'LATINA',
    'FUENCARRAL- EL PARDO':'FUENCARRAL-EL PARDO',
    'TETUÁN':'TETUAN',
    'VICÁLVARO':'VICALVARO',
    'CHAMARTÍN':'CHAMARTIN',
    'CHAMBERÍ':'CHAMBERI'
}

gdf['DISTRICT'] = gdf['DISTRICT'].replace(corrections)

#Attempt to make invalid geometries valid
gdf['geometry_valid'] = gdf.geometry.make_valid()
print("Number of valid geometries after make_valid():", gdf['geometry_valid'].is_valid.sum())
gdf['geometry'] = gdf['geometry_valid']
gdf = gdf.drop(columns=['geometry_valid'])

#### Save GeoDataFrame on Madrid's map ####
madrid_works = folium.Map(location=[40.4168, -3.7038], zoom_start=11)
folium.GeoJson(gdf).add_to(madrid_works)
gdf.to_file('data/processed/madrid_accessibility_works_map.geojson', driver='GeoJSON')