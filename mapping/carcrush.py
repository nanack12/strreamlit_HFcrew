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

ta_data = pd.read_csv('./csv/transat.csv', encoding='utf8',engine='python')
ta_data.info()

i=0
custom_icon_path0 = './png/sign0.png'
custom_icon_path1 = './png/sign1.png'
custom_icon_path2 = './png/sign2.png'
custom_icon_path3 = './png/sign3.png'

for i in range(len(ta_data)):
    lat = ta_data.loc[i,'위도']
    long = ta_data.loc[i, '경도']
    total = int(ta_data.loc[i,'사상자수'])
    die = int(ta_data.loc[i,'사망자수'])
    js = int(ta_data.loc[i,'중상자수'])
    gs = int(ta_data.loc[i,'경상자수'])
    bs = int(ta_data.loc[i, '부상신고자수'])
    
    circle = total + 10
    print(lat,long,total,die,js,gs,bs,circle)

    
    
for i in range(len(ta_data)):
    lat = ta_data.loc[i,'위도']
    long = ta_data.loc[i, '경도']
    total = int(ta_data.loc[i,'사상자수'])
    die = int(ta_data.loc[i,'사망자수'])
    js = int(ta_data.loc[i,'중상자수'])
    gs = int(ta_data.loc[i,'경상자수'])
    bs = int(ta_data.loc[i, '부상신고자수'])
    
    if die > 0:
        folium.Marker(location=[lat, long], tooltip=("사상자수:", total, "\n사망자수:", die, "\n중상자수:", js, "\n경상자수:", gs, "\n부상신고자수:", bs),
                    icon=folium.CustomIcon(icon_image=custom_icon_path1, icon_size=(32, 32))).add_to(map_gangseo)
    elif js > 0:
        folium.Marker(location=[lat, long], tooltip=("사상자수:", total, "\n사망자수:", die, "\n중상자수:", js, "\n경상자수:", gs, "\n부상신고자수:", bs),
                    icon=folium.CustomIcon(icon_image=custom_icon_path3, icon_size=(32, 32))).add_to(map_gangseo)
    elif gs > 0:
        folium.Marker(location=[lat, long], tooltip=("사상자수:", total, "\n사망자수:", die, "\n중상자수:", js, "\n경상자수:", gs, "\n부상신고자수:", bs),
                    icon=folium.CustomIcon(icon_image=custom_icon_path0, icon_size=(32, 32))).add_to(map_gangseo)
    else:
        folium.Marker(location=[lat, long], tooltip=("사상자수:", total, "\n사망자수:", die, "\n중상자수:", js, "\n경상자수:", gs, "\n부상신고자수:", bs),
                    icon=folium.CustomIcon(icon_image=custom_icon_path2, icon_size=(32, 32))).add_to(map_gangseo)

map_gangseo.save('./html/accident_final.html')



