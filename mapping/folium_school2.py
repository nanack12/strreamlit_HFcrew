import pandas as pd
import folium
import geopandas as gpd
import json
import numpy as np
from folium import GeoJson

# 지도 생성
tiles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
attr = "Google"
map_gangseo = folium.Map(location=[37.5612346, 126.8228132], zoom_start=13, tiles=tiles, attr=attr)
map_gangseo.save("./map.html")

# GeoJSON 파일 읽기
geojson_path = './geojson/najs.geojson'
with open(geojson_path, encoding='utf-8') as f:
    data = json.load(f)

# GeoJSON 레이어 생성
geojson_layer = GeoJson(data, style_function=lambda x: {"fillColor": "blue",
                                                                "color": "gray",
                                                                "weight": 1,
                                                                "fillOpacity": 0.1}).add_to(map_gangseo)

# CSV 파일 읽기
GS_geoData = pd.read_csv('./csv/school.csv', encoding='utf-8', engine='python')
GS_geoData.info()

# 마커 생성 및 지도에 추가
for i in range(len(GS_geoData)):
    lat = GS_geoData.loc[i, '위도']
    long = GS_geoData.loc[i, '경도']
    name = GS_geoData.loc[i, '학교명']
    
    folium.Marker([lat, long], tooltip=name, icon=folium.Icon(color='yellow', icon='home')).add_to(map_gangseo)

# 생성된 지도를 HTML 파일로 저장
map_gangseo.save('./html/school_final.html')