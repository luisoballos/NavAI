from shapely.geometry import LineString, Point
import geopandas as gpd
import pandas as pd
import folium

#### Extraction ####
df_sidewalks = gpd.read_file("data/raw/Ancho_aceras/ANCHO_MEDIO_ACERAS.shp")
## Bounding box
## Oeste: -3.888585
## Este: -3.516245
## Sur: 40.311410
## Norte: 40.645133


df_buzzers = pd.read_csv("data/raw/avisadores_acusticos.csv",sep=';')
#### Transformation ####
column_rename = {
    #Sidewalk's columns
    "Ancho_medi":"ANCHO_MEDIO",
    "Shape_STAr":"AREA",
    "Shape_STLe":"LENGTH",

    #Buzzer's columns
    "tipo_elem":"TIPO",     #Tipo de elemento
    "distrito":"DISTRITO",  #Número que identifica el distrito al que pertenece el avisador acústico
    "id":"ID",              #Identificador del avisador acústico (valor único)
    "id_cruce":"ID_CRUCE",  #Identificador del cruce
    "fecha_inst":"FECHA",   #Fecha de instalación del elemento
    "utm_x":"UTM_X",        #Coordenada X del punto que indica la representación del avisador acústico en el sistema de referencia de coordenadas ETRS89 / UTM zone 30N (EPSG: 25830)
    "utm_y":"UTM_Y",        #Coordenada Y del punto que indica la representación del avisador acústico en el sistema de referencia de coordenadas ETRS89 / UTM zone 30N (EPSG: 25830)
    "longitud":"LONGITUD",  #Coordenada X del punto que indica la representación del avisador acústico en el sistema de referencia de coordenadas WGS 84 (EPSG: 4326) 
    "latitud":"LATITUD"     #Coordenada Y del punto que indica la representación del avisador acústico en el sistema de referencia de coordenadas WGS 84 (EPSG: 4326) 
}

df_sidewalks = df_sidewalks.rename(columns=column_rename)
df_buzzers = df_buzzers.rename(columns=column_rename)

#Change buzzer type names
df_buzzers['TIPO'] = df_buzzers['TIPO'].replace({
    'AVISADOR ACUSTICO (ANTIGUO - RELOJ INDEPENDIENTE O MECANICO)': 'ANTIGUO',
    'AVISADOR ACUSTICO (MODERNO - DIGITAL PROGRAMABLE - BLUETOOTH)': 'MODERNO/BLUETOOTH',
    'AVISADOR ACUSTICO (MODERNO - DIGITAL PROGRAMABLE)': 'MODERNO'
})

#Change district names
df_buzzers['DISTRITO'] = df_buzzers['DISTRITO'].replace({
    1:'CENTRO',
    2:'ARGANZUELA',
    3:'RETIRO',
    4:'SALAMANCA',
    5:'CHAMARTIN',
    6:'TETUAN',
    7:'CHAMBERI',
    8:'FUENCARRAL-EL PARDO',
    9:'MOCLOA-ARAVACA',
    10:'LATINA',
    11:'CARABANCHEL',
    12:'USERA',
    13:'PUENTE DE VALLECAS',
    14:'MORATALAZ',
    15:'CIUDAD LINEAL',
    16:'HORTALEZA',
    17:'VILLAVERDE',
    18:'VILLA DE VALLECAS',
    19:'VICALVARO',
    20:'SAN BLAS-CANILLEJAS',
    21:'BARAJAS'
})

#Remove NAs
df_buzzers = df_buzzers.dropna()

#Change 'FECHA' to datetime type
df_buzzers['FECHA'] = pd.to_datetime(df_buzzers['FECHA'], errors='coerce')

#Add antiqueness column
df_buzzers['ANTIGUEDAD'] = (pd.to_datetime('now') - df_buzzers['FECHA']).dt.days / 365.25

#Save datasets as geodataframes
df_sidewalks.to_file('data/processed/gdf_sidewalks.geojson', driver='GeoJSON')
geometry_buzzers = [Point(xy) for xy in zip(df_buzzers['LONGITUD'], df_buzzers['LATITUD'])]
gdf_buzzers = gpd.GeoDataFrame(df_buzzers, geometry=geometry_buzzers, crs="EPSG:4326")
gdf_buzzers.to_file('data/processed/gdf_buzzers.geojson', driver='GeoJSON')