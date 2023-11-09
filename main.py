import streamlit as st
from streamlit_option_menu import option_menu
import project, detai
import pandas as pd
import os
import datetime

def getData(data_path):
    df_total = []
    for file in os.listdir(data_path):
        if file.endswith('.csv.tar.gz'):
            file = data_path + file
            df = pd.read_csv(file,dtype='unicode',compression='gzip')
            df_total.append(df)
            df_output = pd.concat(df_total)
    return df_output
df = getData('D:/J&T/FORECAST/BI/ORDER/')
df['date'] = pd.to_datetime(df['date'])
df['total_order'] = df['total_order'].astype(int)
latest_year = df['date'].dt.year.max()
latest_month = df[df['date'].dt.year == latest_year]['date'].dt.month.max()
multi_day = df[(df['date'].dt.year == latest_year) & (df['date'].dt.month == latest_month)]['date'].dt.day.unique()
latest_day = df[(df['date'].dt.year == latest_year) & (df['date'].dt.month == latest_month)]['date'].dt.day.max()
df.loc[df['ma_khach_hang'].str[:3] == '084', 'KH'] = 'HQ'
df.loc[~(df['ma_khach_hang'].str[:3] == '084'), 'KH'] = 'KV'


st.set_page_config(
    page_title = "J&T",
)


class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, function):
        self.apps.append({
            'title': title,
            'function': function
        })
    def run():
        st.markdown(f"""
            <style>
                .block-container{{
                    max-width: 1200px!important;
                }}
            </style>  
            """, unsafe_allow_html=True)
        
        with st.sidebar:
            app = option_menu(
            menu_title = None,
            options = ['Chart','Detai'],
            icons = ['house-fill','person-circle'],
            # menu_icon = 'chat-text-fill',
            menu_icon = 'cast',
            default_index = 0,
            styles = {
                'container':{'padding':'5!important','background-color':'black'},
                'icon':{'color':'white','font-size':'23px'},
                'nav-link':{'color':'white','font-size':'20px','text-align':'left','margin':'0px'},
                'nav-link-selected':{'background-color':'#02ab21'},
            }
        )
        
        # Sử dụng  phía trên bên ngoài sidebar bên trái
        # app = option_menu(
        #     menu_title = None,
        #     options = ['Chart','About'],
        #     icons = ['house-fill','person-circle'],
        #     # menu_icon = 'chat-text-fill',
        #     menu_icon = 'cast',
        #     default_index = 0,
        #     orientation = 'horizontal',
        #     styles = {
        #         'container':{'padding':'5!important','background-color':'black'},
        #         'icon':{'color':'white','font-size':'23px'},
        #         'nav-link':{'color':'white','font-size':'20px','text-align':'left','margin':'0px'},
        #         'nav-link-selected':{'background-color':'#02ab21'},
        #     }
        # )
        
        st.sidebar.header("Filter Here:")
        # year=st.sidebar.multiselect(
        #     "Select the year",
        #     options=df['date'].dt.year.unique(),
        #     default=[latest_year]
        # )
        st.markdown(
            f"""<style>
                div[data-widget="st-dateslider"] .stDateInput input[type="date"] {{
                    width: 200px;                    
                }}
            </style>""",
            unsafe_allow_html=True,
        )
        first_date=st.sidebar.date_input(
            "Select a date",
            datetime.date(latest_year,latest_month,1)
        )
        latest_date=st.sidebar.date_input(
            "Select a date",
            datetime.date(latest_year,latest_month,latest_day)
        )
        customer = st.sidebar.multiselect(
            "Select HQ or KV",
            df['KH'].unique(),
            'HQ'
        )
        if 'HQ' in customer:
            id_kh = df[df['KH']=='HQ']['ma_khach_hang'].unique()
        elif 'KV' in customer:
            id_kh = df[df['KH']=='KV']['ma_khach_hang'].unique()
        else:
            id_kh = df['ma_khach_hang'].unique()
        if 'HQ' in customer:
            ne_kh = df[df['KH']=='HQ']['nguon_dat_hang'].unique()
        elif 'KV' in customer:
            ne_kh = df[df['KH']=='KV']['nguon_dat_hang'].unique()
        else:
            ne_kh = df['nguon_dat_hang'].unique()
        st.markdown("""
            <style>
            .stMultiSelect {
                height: 68px !important;
                overflow: auto;
            }
            </style>
            """, unsafe_allow_html=True)
        id_kh = st.sidebar.multiselect(
        "Select ID KH",
        id_kh,
        id_kh
        )
        ne_kh = st.sidebar.multiselect(
        "Select name KH",
        ne_kh
        )
        
        
        if app == 'Chart':
            project.app(df, first_date, latest_date, customer, id_kh, ne_kh)
        if app == 'Detai':
            detai.app( first_date, latest_date, customer, id_kh, ne_kh)
        st.markdown("""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """, unsafe_allow_html=True)
    run()