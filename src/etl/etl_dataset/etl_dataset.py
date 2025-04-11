import geopandas as gpd
import pandas as pd
import folium

gdf20 = gpd.read_file("C:/Users/luiso/OneDrive/Documents/Bootkampf/Proyecto final/data/raw/Accesibilidad_2020/Accesibilidad.shp")
gdf21 = gpd.read_file("C:/Users/luiso/OneDrive/Documents/Bootkampf/Proyecto final/data/raw/Accesibilidad_2021/ACCESIBILIDAD_ACERAS_2021.shp")
gdf24 = gpd.read_file("C:/Users/luiso/OneDrive/Documents/Bootkampf/Proyecto final/data/raw/Accesibilidad_2024/ACCESIBILIDAD_ACERAS_2024.shp")

# Transform
gdf20.columns = [i.upper() for i in gdf20.columns]
gdf21.columns = [i.upper() for i in gdf21.columns]
gdf24.columns = [i.upper() for i in gdf24.columns]

gdf20 = gdf20.rename(columns={"CALZADA_M2":"ROAD_AREA","DISTRITO":"DISTRICT","P_P_NUEVOS":"NEW_SIDEWALKS","P_P_RENOVA":"RENEWED_SIDEWALKS","ACERA_M2":"SIDEWALKS_AREA"})
gdf21 = gdf21.rename(columns={"PASPEA_NUE":"NEW_SIDEWALKS","PASPEA_REN":"RENEWED_SIDEWALKS","SUP_CALZAD":"ROAD_AREA","SUP_ACERA":"SIDEWALKS_AREA","DISTRITO":"DISTRICT"})
gdf24 = gdf24.rename(columns={"DISTRITOTX":"DISTRICT","SUPCALZADA":"ROAD_AREA","SUPACERA":"SIDEWALKS_AREA", "PASOSNUEVO":"NEW_SIDEWALKS","PASOSRENOV":"RENEWED_SIDEWALKS"})

gdf20 = gdf20[['DISTRICT','ROAD_AREA','SIDEWALKS_AREA','NEW_SIDEWALKS','RENEWED_SIDEWALKS','GEOMETRY']]
gdf21 = gdf21[['DISTRICT','ROAD_AREA','SIDEWALKS_AREA','NEW_SIDEWALKS','RENEWED_SIDEWALKS','GEOMETRY']]
gdf24 = gdf24[['DISTRICT','ROAD_AREA','SIDEWALKS_AREA','NEW_SIDEWALKS','RENEWED_SIDEWALKS','GEOMETRY']]

gdf20['YEAR'] = 2020
gdf21['YEAR'] = 2021
gdf24['YEAR'] = 2024

# Standardize columns before concatenation
common_columns = list(set(gdf20.columns) & set(gdf21.columns) & set(gdf24.columns))

gdf20_std = gdf20[common_columns].copy()
gdf21_std = gdf21[common_columns].copy()
gdf24_std = gdf24[common_columns].copy()

# Ensure geometry consistency
for df in [gdf20_std, gdf21_std, gdf24_std]:
    geom_col = [col for col in df.columns if df[col].dtype == 'geometry'][0]
    if geom_col != 'geometry':
        df.rename(columns={geom_col: 'geometry'}, inplace=True)
        df.set_geometry('geometry', inplace=True)
    
    df.set_crs("EPSG:25830", allow_override=True, inplace=True)

# Concatenate
gdf = gpd.GeoDataFrame(
    pd.concat([gdf20_std, gdf21_std, gdf24_std], ignore_index=True),
    geometry='geometry'
)

# Save CSV
gdf.to_csv('dataset.csv', index=False)

# Centrar el mapa en Madrid
madrid_map = folium.Map(location=[40.4168, -3.7038], zoom_start=11)

# Añadir capa GeoJSON
folium.GeoJson(gdf).add_to(madrid_map)
madrid_map