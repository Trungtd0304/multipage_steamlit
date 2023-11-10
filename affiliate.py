import streamlit as st
import pandas as pd

def app(df, first_date, latest_date, customer, id_kh, ne_kh,id_kv,id_tinh):
    df=df.query(
        "date >= @first_date & date <= @latest_date & (khu_vuc == @id_kv | tinh_gui == @id_tinh)"
    )
    mapping = {'TPOS':'TPOS','UPOS':'UPOS','EVOSHOP':'UPOS','SAPOAFFILIATE':'SAPO','PANCAKE':'PANCAKE','NHANHMOIGIOI':'NHANH','KIOTVIETMOIGIOI':'KIOTVIET','HARAVAN':'HARAVAN'}
    df['affiliate'] = df['nguon_dat_hang'].map(mapping)
    rename_cot = {  'khu_vuc': 'Khu vực', 
                'tinh_gui': 'Tỉnh gửi'}
    df = df.rename(columns=rename_cot)
    df_pivot_KV_number = pd.pivot_table(data=df,index=['Khu vực'], columns='affiliate', values='total_order',aggfunc=sum,fill_value=0)
    df_pivot_KV_number['Tổng'] = df_pivot_KV_number.iloc[:, 0:].sum(axis=1)
    # Thêm % total_order theo Khu vực
    df_pivot_KV_Ratio= pd.pivot_table(data=df, index='Khu vực',
                                columns='affiliate',
                                values='total_order',
                                aggfunc=sum,
                                fill_value=0).apply(lambda x: round(x*100/sum(x),2))
    total = df_pivot_KV_number['Tổng'].sum()
    df_pivot_KV_Ratio['Tỷ lệ %'] = df_pivot_KV_number['Tổng'].apply(lambda x: round(x/total*100,2))
    # By tỉnh gửi
    df_pivot_Tinh_number = pd.pivot_table(data=df,index=['Tỉnh gửi'], columns='affiliate', values='total_order',aggfunc=sum,fill_value=0)
    df_pivot_Tinh_number['Tổng'] = df_pivot_Tinh_number.iloc[:, 0:].sum(axis=1)
    df_pivot_Tinh_Ratio= pd.pivot_table(data=df, index='Tỉnh gửi',
                                columns='affiliate',
                                values='total_order',
                                aggfunc=sum,
                                fill_value=0).apply(lambda x: round(x*100/sum(x),2))
    total = df_pivot_Tinh_number['Tổng'].sum()
    df_pivot_Tinh_Ratio['Tỷ lệ %'] = df_pivot_Tinh_number['Tổng'].apply(lambda x: round(x/total*100,2))
    tab1, tab2, tab3, tab4= st.tabs(['Total order by region','% Order by region','Total order by province','% Order by province'])
    with tab1:
        st.write(df_pivot_KV_number)
    with tab2:
        st.write(df_pivot_KV_Ratio)
    with tab3:
        st.write(df_pivot_Tinh_number)
    with tab4:
        st.write(df_pivot_Tinh_Ratio)