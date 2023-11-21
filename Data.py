import streamlit as st
import folium
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import requests
import plotly.express as px
import plotly.graph_objects as go
import base64
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
from PIL import Image
from plotly.subplots import make_subplots

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/SKTE40H.png);
                background-repeat: no-repeat;
                background-position: 45px 45px;
                background-size:auto;
                padding-top: 185px;
                margin-bottom:20px;

            }
            [data-testid="stSidebarNav"]::before {
                content: "Created by ©HFCREW";
                margin-left: 117px;
                margin-top: 30px;
                background-position: 100px 100px;
                font-size: 10px;
                position: relative;
                top: 88px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar():
    with st.sidebar:
        selected = option_menu("데이터", ["cctv", "교통량", "어린이 사고","어린이 보호구역","초/중/고 위치"], 
        icons=['bi bi-camera-video-fill', 'bi bi-car-front-fill','bi bi-bandaid-fill','bi bi-sign-stop-fill','bi bi-hospital-fill'],
        menu_icon="bi bi-bar-chart-line-fill", 
        default_index=0,
        styles = {
        "container": {"padding": "4!important"},
        "icon": {"color": "white", "font-size": "25px"},
        "nav-link": {"font-size": "16px", 
                    "text-align": "left", 
                    "margin":"0px", 
                    "--hover-color": "#FEEFC6",
                    "color": "white"
                    },
        "nav-link:hover": {"color": "#0b1e33"},
        "nav-link-selected": {"background-color": "#FCCF55",
                                "color": "#0b1e33"},
    })

    return selected    

def main_header(page):
    st.title("강서구 어린이 교통환경 데이터 시각화")
    st.subheader("3조🦷틀딱코딩단")

def load_folium_map(selected_page):

    if selected_page == "cctv":
        html_file_path = "./html/cctv_final.html"
    elif selected_page == "교통량":
        html_file_path = "./html/traffic_final.html"
    elif selected_page == "어린이 사고":
        html_file_path = "./html/accident_final.html"
    elif selected_page == "어린이 보호구역":
        html_file_path = "./html/childrenArea_final.html"
    elif selected_page == "초/중/고 위치":
        html_file_path = "./html/school_final.html"     
    else:
        # 지도가 선택되지 않은 경우의 기본값
        html_file_path = ""

    # 선택한 인덱스에 따라 Folfum 지도를 표시
    if html_file_path:
        with open(html_file_path, "r", encoding="utf-8") as file:
            folium_html_content = file.read()
            st.components.v1.html(folium_html_content, height=600, scrolling=True)
    else:
        st.warning("지도를 선택해주세요.")
    

def plotly(selected_page):
    if selected_page == "cctv":
            line_counter = 0
            fieldName = []
            cctvList = []
            with open('./csv/test1.csv', 'r', encoding='utf8') as cd:
                while 1:
                    data = cd.readline()
                    if not data:
                        break
                    if line_counter == 0:
                        fieldName = data.split(",")
                    else:
                        cctvList = data.split(",")
                    line_counter += 1
            data = {'Category': fieldName[2:], 'Value': cctvList[2:]}
            df = pd.DataFrame(data)

            fig = px.pie(df, values='Value', names='Category',title='강서구 목적별 CCTV 설치 수량',hole=0.3
                        ,color_discrete_sequence=['#463900','#7C6F00','#B2A535','#D6C959','#FAED7D','#FFFFA1','#FFFFB3','#FFFFFF'])  
            st.plotly_chart(fig,use_container_width=True)

    elif selected_page == "초/중/고 위치":
            data = pd.read_csv('./csv/school.csv',encoding='utf-8',engine='python')

            i=0
            schoolType=[]

            for i in range(len(data)):
                schoolType+=[data.loc[i, '학교종류명']]

            i=0
            element=[]
            middle=[]
            high=[]
            etcs=[]
            colors = ['#FFA2FF', '#B95AFF', '#9536FF', '#5F00FF']
            for i in range(len(schoolType)):
                if schoolType[i]=='초등학교':
                    element+=[schoolType[i]]
                elif schoolType[i]=='중학교':
                    middle+=[schoolType[i]]
                elif schoolType[i]=='고등학교':
                    high+=[schoolType[i]]
                else:
                    etcs+=[schoolType[i]]
            
            SchoolType=['초등학교','중학교','고등학교','특수/기타']
            DataSet=[len(element),len(middle),len(high),len(etcs)]
            df= pd.DataFrame({'Category':SchoolType,'Value':DataSet,'Colors':colors})

            fig=px.bar(df,x='Category',y='Value',color='Colors', color_discrete_sequence=colors,title='강서구 내 학교 종류별 숫자',text='Value')

            fig.update_layout(
                xaxis_title='학교 구분',
                yaxis_title='학교 수',
                legend_title='학교 구분'
                )
            fig.data[0].name = '초등학교'
            fig.data[1].name = '중학교'
            fig.data[2].name = '고등학교'
            fig.data[3].name = '특수/기타학교'
            fig.update_traces(textposition='outside', textfont=dict(color='black'))
            st.plotly_chart(fig)

    elif selected_page == "교통량":
            part1=[]
            count1=[]
            lineCounter=0

            with open('./csv/trafficTotal.csv','r',encoding='utf8')as csvList:
                while 1:
                    data=csvList.readline()
                    if not data:break
                    if lineCounter == 0:
                        part1=data.split(",")

                    else:
                        count1.append(data.split(","))

                    lineCounter+=1

            part2=[]
            count2=[]
            lineCounter=0

            with open('./csv/trafficGangseo.csv','r',encoding='utf8')as csvList1:
                while 1:
                    data=csvList1.readline()
                    if not data:break
                    if lineCounter == 0:
                        part2=data.split(",")

                    else:
                        count2.append(data.split(","))

                    lineCounter+=1

            chart1=[]
            chart2=[]
            i=0

            count1 = [item for sublist in count1 for item in sublist]
            chart1=count1[0::2]
            count1=[float(i) for i in count1[1::2]]

            count2 = [item for sublist in count2 for item in sublist]
            chart2 = count2[0::2]
            count2=[float(i) for i in count2[1::2]]

            fig2=go.Figure()
                        
            fig2.add_trace(go.Bar(x=chart1,y=count1,name='서울시 교통량 평균',marker_color='yellow'))
            fig2.add_trace(go.Bar(x=chart1,y=count2,name='강서구 교통량 평균',marker_color='orange'))
            fig2.update_layout(title='2022년 강서구 교통량의 평균',xaxis_title='구분',yaxis_title='교통량의 통계',barmode='group')

            st.plotly_chart(fig2)

    elif selected_page == "어린이 사고":
            years=[]
            counts=[]
            lineCounter=0
            with open('./csv/childrenAccidentBar.csv','r',encoding='utf8')as csvList:
                while 1:
                    data=csvList.readline()
                    if not data:break
                    if lineCounter == 0:
                        years=data.split(",")
                    else:
                        counts=data.split(",")
                    
                    lineCounter+=1
            
            years = [int(i) for i in years[1:]]
            counts = [int(i) for i in counts[1:]]
            
            colors=['#FFFF7E','#FFFF48','#FFF612','#C9AE00','#816600']
            df= pd.DataFrame({'Category':years,'Value':counts,'Years':colors})

            fig3=px.bar(df,x='Category',y='Value',color='Years',color_discrete_sequence=colors,title='강서구 어린이 교통사고 년도별 통계',text='Value')

            fig3.update_layout(
                xaxis_title='연도',
                yaxis_title='교통사고 수',
                legend_title='연도 구분')
            
            fig3.update_traces(textposition='outside', textfont=dict(color='black'))
            
            fig3.data[0].name = '2018'
            fig3.data[1].name = '2019'
            fig3.data[2].name = '2020'
            fig3.data[3].name = '2021'
            fig3.data[4].name = '2022'

            st.plotly_chart(fig3)

    elif selected_page == "어린이 보호구역":
            part1 = []
            count1 = []
            line_counter = 0

            with open('./csv/gs_ChildrenTotal.csv', 'r', encoding='utf-8') as csv_list:
                while 1:
                    data = csv_list.readline()
                    if not data:break
                    if line_counter == 0:
                        part1 = data.split(",")
                    else:
                        count1.append(data.split(","))

                    line_counter += 1

            part2=[]
            count2=[]
            line_counter = 0
            with open('./csv/gs_ChildrenSafetyzone.csv', 'r', encoding='utf-8') as csv_list_1:
                while 1:
                    data=csv_list_1.readline()
                    if not data:break
                    if line_counter ==0:
                        part2=data.split(",")
                    else :
                        count2.append(data.split(","))

                    line_counter +=1

            number1 = []
            number2 = []
            year = []
            count1 = [item for sublist in count1 for item in sublist]
            count2 = [item for sublist in count2 for item in sublist]

            number1 = count1[1::2]
            number2 = count2[1::2]
            year = count1[0::2]

            number1 = [int(i) for i in number1[:]]
            number2 = [int(i) for i in number2[:]]
            year = [int(i) for i in year[:]]

            df = pd.DataFrame({'Year': year, 'YouthRatio': number1})
            df1 = pd.DataFrame({'Year': year, 'ChildProtectionArea': number2})

            fig = make_subplots(specs=[[{"secondary_y":True}]])

            fig.add_trace(go.Bar(x=df['Year'], y=df['YouthRatio'], name='청소년 비율',  width=0.7, marker_color='skyblue'), secondary_y=False)
            fig.add_trace(go.Scatter(x=df1['Year'], y=df1['ChildProtectionArea'], mode='lines+markers', name='아동 안전지대', marker=dict(color='orange', size=20, symbol='circle'),line=dict(width=4)),secondary_y=True)

            fig.update_layout(
                title="<b>강서구 청소년 비율 및 어린이보호구역",
                xaxis_title='연도',
                yaxis_title='비율 또는 면적'
            )
            fig.update_layout(width=680, height=400,margin=dict(t=50,b=0,l=0,r=0))
            fig.update_layout(legend=dict(traceorder='normal', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
            fig.update_yaxes(title_text="강서구 거주 인구 중 청소년 비율(%)", secondary_y=False)
            fig.update_yaxes(title_text="어린이 보호구역(개)", secondary_y=True)
            st.plotly_chart(fig,use_container_width=True)

            
def dataframe(selected_page):
    if selected_page=="cctv":
        refined_data = pd.read_csv('./csv/test1.csv')
        st.dataframe(refined_data)
    elif selected_page=="교통량":
        refined_data = pd.read_csv('./csv/trafficTotal.csv')
        st.dataframe(refined_data)    
    elif selected_page =="어린이 사고":
        refined_data = pd.read_csv('./csv/childrenAccidentBar.csv')
        st.dataframe(refined_data)
    elif selected_page =="어린이 보호구역":
        refined_data = pd.read_csv('./csv/gs_ChildrenTotal.csv')
        st.dataframe(refined_data)
    elif selected_page =="초/중/고 위치":
        refined_data = pd.read_csv('./csv/schoole_count.csv')
        st.dataframe(refined_data)

def set_custom_css():
    st.set_page_config(page_title="강서구 교통환경 시각화", page_icon="🚌", layout="wide")
    st.markdown(
        """
        <style>
            .main {
                padding-top: 0px;
                max-width: 1600px !important;
            }
        </style>
        """,
        unsafe_allow_html=True)

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)   


set_custom_css()


add_logo()                
selected_page = sidebar()
main_header(selected_page)
st.divider()

col1, col2_and_col3 = st.columns([1, 0.8])  



with col1:
    load_folium_map(selected_page)
    
    
with col2_and_col3:
    plotly(selected_page)

    dataframe(selected_page)

