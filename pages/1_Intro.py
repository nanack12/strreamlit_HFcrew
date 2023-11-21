import pandas as pd 
import json 
import requests 
import numpy as np
import streamlit as st
from PIL import Image
from tkinter.tix import COLUMN
from pyparsing import empty
import folium
import plotly.express as px 

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

def set_custom_css():
    st.set_page_config(page_title="강서구 교통환경 시각화", page_icon="🚌", layout="wide")
    padding_top=0
    st.markdown(
        """
        <style>
            .main {
                padding-top:{padding_top}rem;
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