import streamlit as st
import pandas as pd
import os
import datetime


def app(df, first_date, latest_date, customer, id_kh, ne_kh,id_kv,id_tinh):
    df['date'] = pd.to_datetime(df['date'])
    # df['total_order'] = df['total_order'].astype(int)
    df=df.query(
        "date >= @first_date & date <= @latest_date & KH == @customer & (ma_khach_hang == @id_kh | nguon_dat_hang == @ne_kh) & (khu_vuc == @id_kv | tinh_gui == @id_tinh)"
    )
    df_selection = df.groupby(['ma_khach_hang','nguon_dat_hang', 'date'])['total_order'].sum().reset_index()
    df_selection['date']=df_selection['date'].dt.strftime('%Y/%m/%d')
    # df_selection['total_order']=df_selection['total_order'].apply('{:,.0f}'.format)
    df_pivot = df_selection.pivot(index=['nguon_dat_hang','ma_khach_hang'], columns='date', values='total_order').reset_index().fillna(0)
    # Tính tổng cho từng dòng và thêm cột tổng vào cuối
    df_pivot['Tổng'] = df_pivot.iloc[:, 2:].sum(axis=1)
    st.write(df_pivot)