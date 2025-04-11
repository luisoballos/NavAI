import geopandas as gpd
import pandas as pd
import webbrowser
import folium

gdf20 = gpd.read_file("C:/Users/luiso/OneDrive/Documents/Bootkampf/NavAI/data/raw/Accesibilidad_2020/Accesibilidad.shp")
gdf21 = gpd.read_file("C:/Users/luiso/OneDrive/Documents/Bootkampf/NavAI/data/raw/Accesibilidad_2021/ACCESIBILIDAD_ACERAS_2021.shp")
gdf24 = gpd.read_file("C:/Users/luiso/OneDrive/Documents/Bootkampf/NavAI/data/raw/Accesibilidad_2024/ACCESIBILIDAD_ACERAS_2024.shp")

### Transform ###
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

# Save CSV
gdf.to_csv('../../data/processed/dataset.csv', index=False)

# Centrar el mapa en Madrid
madrid_map = folium.Map(location=[40.4168, -3.7038], zoom_start=11)

# Añadir capa GeoJSON
folium.GeoJson(gdf).add_to(madrid_map)
madrid_map.save("../../img/madrid_map.html")
webbrowser.open("madrid_map.html")
import webbrowser
import os

file_path = os.path.abspath("madrid_map.html")
webbrowser.get(using='windows-default').open(f"file://{file_path}")

### EDA ###
gdf['DISTRICT'].unique()
gdf.info()

gdf.dtypes
gdf.isnull().sum()
gdf['DISTRICT'].value_counts(dropna=False)
gdf['YEAR'].value_counts()

gdf.groupby('YEAR')[['NEW_SIDEWALKS', 'RENEWED_SIDEWALKS', 'SIDEWALKS_AREA', 'ROAD_AREA']].sum()
df.groupby(['DISTRICT', 'YEAR'])[['NEW_SIDEWALKS', 'RENEWED_SIDEWALKS']].sum().unstack()
gdf.corr(numeric_only=True)

### Statistics ###
import seaborn as sns
import matplotlib.pyplot as plt

gdf.describe()

corr_matrix = gdf[['ROAD_AREA','SIDEWALKS_AREA','NEW_SIDEWALKS','RENEWED_SIDEWALKS']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()