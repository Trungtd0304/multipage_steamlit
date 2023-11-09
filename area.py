import streamlit as st
import pandas as pd

def app(df, first_date, latest_date, customer, id_kh, ne_kh,id_kv,id_tinh):
    df=df.query(
        "date >= @first_date & date <= @latest_date & KH == @customer & (ma_khach_hang == @id_kh | nguon_dat_hang == @ne_kh) & (khu_vuc == @id_kv | tinh_gui == @id_tinh)"
    )

    df_selection = df.groupby(['khu_vuc', 'date'])['total_order'].sum().reset_index()
    df_selection['date']=df_selection['date'].dt.strftime('%Y/%m/%d')
    df_pivot_KV_number = pd.pivot_table(data=df_selection,index=['khu_vuc'], columns='date', values='total_order',aggfunc=sum,fill_value=0)
    df_pivot_KV_number['Tổng'] = df_pivot_KV_number.iloc[:, 0:].sum(axis=1)
    # st.write(df_pivot_KV_number)    
    # Thêm % total_order theo khu_vuc
    df_pivot_KV_Ratio= pd.pivot_table(data=df_selection, index='khu_vuc',
                                columns='date',
                                values='total_order',
                                aggfunc=sum,
                                fill_value=0).apply(lambda x: round(x*100/sum(x),2))
    total = df_pivot_KV_number['Tổng'].sum()
    df_pivot_KV_Ratio['Tỷ lệ %'] = df_pivot_KV_number['Tổng'].apply(lambda x: round(x/total*100,2))
    # st.write(df_pivot_KV_Ratio)
    c1, c2 = st.columns(2)
    c1.write(df_pivot_KV_number)  
    c2.write(df_pivot_KV_Ratio)