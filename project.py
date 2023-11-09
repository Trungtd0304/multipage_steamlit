import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def app(df, first_date, latest_date, customer, id_kh, ne_kh,id_kv,id_tinh):
    df['Mã tình'] = df['ma_khach_hang'].str.slice(0, 3)
    df['date'] = df['date'].dt.date
    df_selection = df.query(
        "date >= @first_date & date <= @latest_date & KH == @customer & (ma_khach_hang == @id_kh | nguon_dat_hang == @ne_kh) & (khu_vuc == @id_kv | tinh_gui == @id_tinh)"
    )
    df_line = df.query(
        "KH == @customer & (ma_khach_hang == @id_kh | nguon_dat_hang == @ne_kh) & (khu_vuc == @id_kv | tinh_gui ==@id_tinh)"
    ).groupby('date')['total_order'].sum().reset_index()
    df_line['ratio_dif'] = ((df_line['total_order']/df_line['total_order'].shift(1))-1)
    df_line['ratio_dif'] = df_line['ratio_dif'].apply(lambda x: '{:.1%}'.format(x))    
    df_line=df_line.query("date >= @first_date & date <= @latest_date")
    # fig_line = px.line(df_line, x='date', y='total_order', labels={'total_order': 'Tổng đơn hàng'})
    # Tạo figure với trục y phụ
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
    go.Scatter(x=df_line['date'], y=df_line['total_order'],text='total_order', name='Total order'),
    secondary_y=False,)
    # Thêm dữ liệu cho trục y phụ
    fig.add_trace(
    go.Scatter(x=df_line['date'], y=df_line['ratio_dif'], name='Tỷ lệ',text='ratio_dif'),
    secondary_y=True,)
    fig.update_layout(title_text='So sánh tổng đơn hàng Ngày và Tỷ lệ thay đổi')
    fig.update_yaxes(range=[min(df_line['total_order'])/1.2, max(df_line['total_order'])*1.2], secondary_y=False)
    # fig.update_yaxes(range=[min(df_line['ratio_dif']), max(df_line['ratio_dif'])], secondary_y=True)
    fig.update_traces(textposition='top center')
    
    
    fig_pie = px.pie(df_selection, names='tinh_gui', values='total_order', title='Tỷ lệ tổng đơn hàng theo tỉnh/thành phố') 
    # Lấy top 5 giá trị lớn nhất
    top5 = df_selection.nlargest(5, 'total_order')['tinh_gui']
    fig_pie.update_traces(pull=0.2, textposition='inside', 
                    textinfo='label+percent' if df_selection['tinh_gui'].isin(top5).any() else 'none')
    df_selection = df_selection.groupby('nguon_dat_hang')['total_order'].sum().reset_index()
    df_selection = df_selection.sort_values(by='total_order', ascending=True)
    df_selection['total_order'] = df_selection['total_order'].apply(lambda x: '{:,.0f}'.format(x))
    fig_bar = px.bar(df_selection, x='total_order', y='nguon_dat_hang', orientation='h', text='total_order', title='Tổng đơn hàng theo khách hàng')
    fig_bar.update_yaxes(tickfont=dict(size=10))
    fig_bar.update_traces(texttemplate='%{text}', textposition='outside')
    layout_params = dict(
    width=500,
    height=600,
    yaxis_title=None,
    xaxis_title=None,
    )
    fig_pie.update_layout(**layout_params)
    fig_bar.update_layout(**layout_params)
    c1, c2 = st.columns(2)
    c1.plotly_chart(fig_pie) 
    c2.plotly_chart(fig_bar)
    st.plotly_chart(fig, use_container_width=True)
