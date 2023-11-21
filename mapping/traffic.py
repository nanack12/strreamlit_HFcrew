#step3, step4, step5, step6, step11 바꾸심 됩니다. 경로 포함해서 바꿔주세요 필요한 파일은 해당 파일 확장자 폴더에 넣으셔서 경로 지정하심됩니다.

#[step2] 필요 라이브러리 임포트
import pandas as pd
import folium
import geopandas as gpd
import json
import numpy as np
from folium import GeoJson


#[step3] map.html 생성 및 저장: location 값은 지도에서 중심이 될 값(강서구청으로 임의 지정) zoom_start는 13
# 구글 지도 타일 설정
tiles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
# 속성 설정
attr = "Google"
#[step3] map.html 생성 및 저장: location 값은 지도에서 중심이 될 값(강서구청으로 임의 지정) zoom_start는 13
map_gangseo=folium.Map(location=[37.5612346, 126.8228132],zoom_start=13, tiles = tiles, attr = attr)
map_gangseo.save("./map.html")


#[step4] 구, 동을 표현할 GeoJSON 파일 로드
geojson_path = './geojson/najs.geojson'
with open(geojson_path, encoding='utf-8') as f:
    data = json.load(f)


#[step5] GeoJson 라이브러리 이용하여 지도에 추가. fillColor-채울 색/color-회색/weight-선굴기/fillOpacity-채울 색의 투명도
geojson_layer = GeoJson(data, style_function=lambda x: {"fillColor": "blue",
                                                                "color": "gray",
                                                                "weight": 1,
                                                                "fillOpacity": 0.1}).add_to(map_gangseo)



#[step6] 데이터를 지도에 나타내기 위한 csv파일 읽어오기, 칼럼의 정보(데이터 타입 등) 을 확인하기 위해 .info()사용
GS_geoData=pd.read_csv('./csv/gangseo_trafic.csv', encoding='utf-8',engine='python')
GS_geoData.info()


#[step7] for 문의 초깃값 지정
i=0


#[step8] (*필수아님)csv 파일의 데이터 확인
for i in range(len(GS_geoData)):
    lat = GS_geoData.loc[i, '위도']
    long = GS_geoData.loc[i, '경도']
    name=GS_geoData.loc[i,'지점명']
    circle=GS_geoData.loc[i,'radius']


    print(name, lat, long, circle)


#[step9] for 문으로 지도에 원 표시하기. CircleMaker([위도,경도],tooltip=마우스 오버했을때 띄울 데이터, color='원테두리', fill='채울 색', fill_opacity=투명도
for i in range(len(GS_geoData)):
    lat = GS_geoData.loc[i, '위도']
    long = GS_geoData.loc[i, '경도']
    name=GS_geoData.loc[i,'지점명']
    circle=GS_geoData.loc[i,'radius']
    
    folium.CircleMarker([lat, long],tooltip= name, radius=circle,color='red',fill='red', fill_opacity=0.6).add_to(map_gangseo)    

#[step11] 완성된 맵 저장.
map_gangseo.save('./html/traffic_final.html')




