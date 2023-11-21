import pandas as pd
import folium
import geopandas as gpd
import json
import numpy as np
from folium import GeoJson

tiles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
attr = "Google"

map_gangseo=folium.Map(location=[37.5612346, 126.8228132],zoom_start=13, tiles = tiles, attr = attr)
map_gangseo.save("./map.html")


geojson_path = './geojson/najs.geojson'
with open(geojson_path, encoding='utf-8') as f:
    data = json.load(f)

geojson_layer = GeoJson(data, style_function=lambda x: {"fillColor": "blue",
                                                                "color": "gray",
                                                                "weight": 1,
                                                                "fillOpacity": 0.1}).add_to(map_gangseo)


GS_geoData=pd.read_csv('./csv/gangseo_cctv.csv', encoding='utf-8',engine='python')
GS_geoData.info()

i=0

for i in range(len(GS_geoData)):
    lat = GS_geoData.loc[i, '위도']
    long = GS_geoData.loc[i, '경도']
    name=GS_geoData.loc[i, '안심 주소']
    circle=int(GS_geoData.loc[i,'CCTV 수량'])
    
    folium.CircleMarker([lat, long], tooltip= name, radius=circle, color='#fb8500',fill="#fb8500").add_to(map_gangseo)    

map_gangseo.save('./html/cctv_final.html')






