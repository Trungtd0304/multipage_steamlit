import streamlit as st
from streamlit_option_menu import option_menu
import project, detai, area, affiliate
import pandas as pd
import os
import datetime

@st.cache_data
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
mapping = {'Hồ Chí Minh':'Hồ Chí Minh','Hà Nội':'Hà Nội','Vĩnh Phúc':'Hà Nội','Thành phố Hà Nội':'Hà Nội',
'Hải Phòng':'Miền Bắc 2','Quảng Ninh':'Miền Bắc 2','Bình Định':'Miền Trung 2','Phú Yên':'Miền Trung 2','Khánh Hòa':'Miền Trung 2','Quảng Ngãi':'Miền Trung 2',
'Quảng Trị':'Miền Trung 1','Thừa Thiên – Huế':'Miền Trung 1','Quảng Nam':'Miền Trung 1','Đà Nẵng':'Miền Trung 1',
'Kon Tum':'Miền Trung 2','Gia Lai':'Miền Trung 2','Đắk Lắk':'Miền Trung 2','Đắk Nông':'Miền Trung 2','Lâm Đồng':'Miền Trung 2',
'Thanh Hóa':'Miền Trung 1','Nghệ An':'Miền Trung 1','Hà Tĩnh':'Miền Trung 1','Quảng Bình':'Miền Trung 1',
'Hà Giang':'Miền Bắc 1','Tuyên Quang':'Miền Bắc 1','Cao Bằng':'Miền Bắc 1','Bắc Kạn':'Miền Bắc 1','Bắc Giang':'Miền Bắc 1','Lạng Sơn':'Miền Bắc 1','Thái Nguyên':'Miền Bắc 1','Lai Châu':'Miền Bắc 1','Điện Biên':'Miền Bắc 1','Sơn La':'Miền Bắc 1','Yên Bái':'Miền Bắc 1','Phú Thọ':'Miền Bắc 1','Hòa Bình':'Miền Bắc 1','Lào Cai':'Miền Bắc 1',
'Hà Nam':'Miền Bắc 2','Ninh Bình':'Miền Bắc 2','Thái Bình':'Miền Bắc 2','Nam Định':'Miền Bắc 2','Hải Dương':'Miền Bắc 2','Hưng Yên':'Miền Bắc 2','Bắc Ninh':'Miền Bắc 2',
'Tây Ninh':'Miền Nam 1','Bình Phước':'Miền Nam 1','Bình Dương':'Miền Nam 1','Đồng Nai':'Miền Nam 1','Bà Rịa – Vũng Tàu':'Miền Nam 1','Ninh Thuận':'Miền Nam 1','Bình Thuận':'Miền Nam 1',
'Đồng Tháp':'Miền Nam 2','Long An':'Miền Nam 2','An Giang':'Miền Nam 2','Kiên Giang':'Miền Nam 2','Hậu Giang':'Miền Nam 2','Cần Thơ':'Miền Nam 2',
'Tiền Giang':'Miền Nam 2','Bến Tre':'Miền Nam 2','Trà Vinh':'Miền Nam 2','Sóc Trăng':'Miền Nam 2','Vĩnh Long':'Miền Nam 2','Bạc Liêu':'Miền Nam 2','Cà Mau':'Miền Nam 2'}
df['khu_vuc'] = df['tinh_gui'].map(mapping)


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
            options = ['Chart','Detai','Area','Affiliate'],
            icons = ['house-fill','person-circle','collection-fill','sliders2'],
            # menu_icon = 'chat-text-fill',
            menu_icon = 'cast',
            default_index = 0,
            styles = {
                'container':{'padding':'1!important','background-color':'black'},
                'icon':{'color':'white','font-size':'10px'},
                'nav-link':{'color':'white','font-size':'15px','text-align':'left','margin':'0px'},
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
        # first_date=st.sidebar.date_input(
        #     "Chọn ngày bắt đầu",
        #     datetime.date(latest_year,latest_month,1)
        # )
        # latest_date=st.sidebar.date_input(
        #     "Chọn ngày kết thúc",
        #     datetime.date(latest_year,latest_month,latest_day)
        # )
        with st.sidebar:
            # st.write("Chọn ngày bắt đầu và kết thúc:")
            col1, col2 = st.columns(2)  # Sử dụng beta_columns để tạo 2 cột
            with col1:
                first_date = st.date_input("Bắt đầu", datetime.date(latest_year, latest_month, 1))
            with col2:
                latest_date = st.date_input("Kết thúc", datetime.date(latest_year, latest_month, latest_day))
        customer = st.sidebar.multiselect(
            "Chọn HQ, KV",
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
        "Chọn mã khách hàng",
        id_kh,
        id_kh
        )
        ne_kh = st.sidebar.multiselect(
        "Chọn tên khách hàng",
        ne_kh
        )
        id_kv = st.sidebar.multiselect(
        "Chọn khu vực",
        df['khu_vuc'].unique(),
        df['khu_vuc'].unique()
        )
        id_tinh = st.sidebar.multiselect(
        "Chọn tỉnh gửi",
        df['tinh_gui'].unique()
        )
        if app == 'Chart':
            project.app(df, first_date, latest_date, customer, id_kh, ne_kh, id_kv,id_tinh)
        if app == 'Detai':
            detai.app(df, first_date, latest_date, customer, id_kh, ne_kh, id_kv,id_tinh)
        if app == 'Area':
            area.app(df, first_date, latest_date, customer, id_kh, ne_kh,id_kv,id_tinh)
        if app =='Affiliate':
            affiliate.app(df, first_date, latest_date, customer, id_kh, ne_kh,id_kv,id_tinh)
        
        st.markdown("""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """, unsafe_allow_html=True)
    run()