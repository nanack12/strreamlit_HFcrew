import pandas as pd
import folium
import geopandas as gpd
from folium import GeoJson
import json

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



#[step6] 데이터를 지도에 나타내기 위한 csv파일 읽어오기, 칼럼의 정보(데이터 타입 등) 을 확인하기 위해 .info()사용
childrenArea=pd.read_csv('./csv/childrenArea.csv', encoding='utf-8',engine='python')
childrenArea.info()


i=0
for i in range(len(childrenArea)):
    lat = childrenArea.loc[i, '경도']
    long = childrenArea.loc[i, '위도']
    form = childrenArea.loc[i, '시설구분']
    address = childrenArea.loc[i, '주소']
    
    print(form, lat, long, address)


from IPython.display import Image
import os


os.chdir('./mapping')

current_dir = os.getcwd()

# 커스텀 아이콘 경로 설정
custom_icon_path = '../png/children.png'

markers = []

# childrenArea의 각 위치에 대해 반복
for i in range(len(childrenArea)):
    lat = childrenArea.loc[i, '위도']
    long = childrenArea.loc[i, '경도']
    address = childrenArea.loc[i, '주소']

    # 현재 위치에 대한 마커 생성
    marker = folium.Marker(
        location=[lat, long],
        popup=address,
        tooltip='어린이보호구역',
        icon=folium.CustomIcon(icon_image=custom_icon_path, icon_size=(32, 32))
    )

    # 마커를 리스트에 추가
    markers.append(marker)

# 모든 마커를 지도에 추가
for marker in markers:
    marker.add_to(map_gangseo)

map_gangseo.save('../html/childrenArea_final.html')



