import streamlit as st
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


def app( first_date, latest_date, customer, id_kh, ne_kh):
    df = getData('D:/J&T/FORECAST/BI/ORDER/')
    df['date'] = pd.to_datetime(df['date'])
    df['total_order'] = df['total_order'].astype(int)
    df.loc[df['ma_khach_hang'].str[:3] == '084', 'KH'] = 'HQ'
    df.loc[~(df['ma_khach_hang'].str[:3] == '084'), 'KH'] = 'KV'
    df=df.query(
        "date >= @first_date & date <= @latest_date & KH == @customer & (ma_khach_hang == @id_kh | nguon_dat_hang == @ne_kh)"
    )
    df_selection = df.groupby(['ma_khach_hang','nguon_dat_hang', 'date'])['total_order'].sum().reset_index()
    df_selection['date']=df_selection['date'].dt.date
    df_selection['total_order']=df_selection['total_order'].apply('{:,.0f}'.format)
    df_pivot = df_selection.pivot(index=['ma_khach_hang','nguon_dat_hang'], columns='date', values='total_order').reset_index().fillna(0)
    
    # st.dataframe(df)
    # st.markdown("""
    #         <style>
    #         #stDataFrame {
    #             height: 800px;
    #         }
    #         </style>
    #         """, unsafe_allow_html=True)
    # st.markdown(
    # f'<style>.dataframe {{ height: 800px; }}</style>',
    # unsafe_allow_html=True
    # )
    st.write(df_pivot)

