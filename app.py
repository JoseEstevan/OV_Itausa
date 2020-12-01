import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import plotly.graph_objects as go
from PIL import Image
ALPHAVANTAGE_API_KEY = 'H983JJABQU6EEV35'
ts = TimeSeries(key=ALPHAVANTAGE_API_KEY, output_format='pandas')
cc = CryptoCurrencies(key=ALPHAVANTAGE_API_KEY, output_format='pandas')

resp = requests.get('https://www.alphavantage.co/query', params={
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': 'ITSA4.SA',
    'market': 'BRL',
    'apikey': ALPHAVANTAGE_API_KEY,
    'datatype': 'json',
    'outputsize': "full"})
doc = resp.json()
        
df = pd.DataFrame.from_dict(doc['Time Series (Daily)'], orient='index', dtype=np.float)
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'Data', '4. close': 'Preço', '6. volume': 'Volume'})


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)
def main():
    overview = '[OverView](https://github.com/JoseEstevan/OverView)'
    
    st.title(overview)
    st.subheader('Itaúsa')
    
    menu = ['OverView','Ações','Sobre']
    choice = st.sidebar.selectbox("Menu",menu)
    financ = Image.open('Itasa.jpg')
    
    if choice == 'OverView':
        st.markdown("A Itaúsa (Itaúsa - Investimentos Itaú S/A) é uma holding brasileira, constituída como sociedade anônima de capital aberto e negociada na B3 sob os códigos ITSA3 e ITSA4. \nSua atividade principal é o controle de empresas do setor financeiro, sendo a principal delas o Banco Itaú Unibanco. \nAlém do Itaú Unibanco, a Itaúsa também controla empresas de outros segmentos. Entre essas, estão a Duratex (papel e celulose), Alpargatas (setor de calçados) e a Itautec (empresa de tecnologia da informação). \nAlém do controle das empresas supracitadas, a Itaúsa ainda detém participação na NTS, transportadora de gás natural. As operações controladas pela holding e a participação na NTS fazem da Itaúsa um dos maiores grupos privados do Brasil.")
        st.subheader('Principais produtos e serviços comercializados pela Itaúsa')
        st.markdown('A atividade principal da Itaúsa é controle e gestão de outras empresas. O principal segmento de atuação da empresa é o setor financeiro, por meio do qual, oferta serviços financeiros básicos, operações de crédito, financiamentos até serviços especializados relativos a investimentos. Além do setor financeiro, a Itaúsa controla empresas dos ramos de papel e celulose, calçados, transporte de gás e tecnologia. A gestão dessas companhias faz da Itaúsa um dos principais conglomerados privados no Brasil.')
        st.image(financ, width=1200)
        d = {'Receita Líquida': [5.008, 5.375, 4.969, 4.687, 4.885, 5.021, 5.289, 4.883],'Custos': [3.718, 4.006, 3.674, 3.641, 3.731, 3.767, 3.729, 3.567], 'Lucro Líquido': [10.569, 9.710, 8.263, 8.216, 8.994, 8.161, 6.011,  4.836], 'Ano': [20191231, 20181231, 20171231, 20161231, 20151231 ,20141231, 20131231, 20121231]}
        datad= pd.DataFrame(data=d)
        datad['Ano'] = datad['Ano'].apply(lambda x: pd.to_datetime(int(x), format="%Y%m%d"))  
        graph1 = px.line(datad,x="Ano", y="Receita Líquida", title='Receita Líquida em Bilhões', height=600, width=1000)
        st.plotly_chart(graph1) 
        
        graph2 = px.line(datad,x="Ano", y="Custos", title='Custos em Bilhões', height=600, width=1000)
        st.plotly_chart(graph2) 
        
        graph2 = px.line(datad,x="Ano", y="Lucro Líquido", title='Lucro Líquido em Bilhões', height=600, width=1000)
        st.plotly_chart(graph2) 
        #st.image()
        #st.image([image1,image2])

        
    
    
    elif choice == 'Ações':
        
        df = pd.DataFrame.from_dict(doc['Time Series (Daily)'], orient='index', dtype=np.float)
        df.reset_index(inplace=True)
        df = df.rename(columns={'index': 'Data', '4. close': 'Preço', '6. volume': 'Volume'})
        
        figg = px.line(df, x='Data', y=df['Preço'], title='Valor das Ações', width=1250, height=800)
        figg.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
        ])))
        st.plotly_chart(figg)


        fig = px.line(df, x='Data', y=df['Volume'], title='Volume Negociado', width=1250, height=800)
        fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
        ])))
        st.plotly_chart(fig)


    elif choice == 'Sobre':
        st.header("Sobre")
        st.markdown('Esta aplicação faz parte do meu projeto OverView, que consiste em fazer análises sobre diferentes assuntos, a fim de praticar e testar coisas novas.')
        st.subheader('Redes Sociais')
        
        linkedin = '[LinkedIn](https://www.linkedin.com/in/joseestevan/)'
        st.markdown(linkedin, unsafe_allow_html=True) 
        
        github = '[GitHub](https://github.com/JoseEstevan)'
        st.markdown(github, unsafe_allow_html=True)  

        medium = '[Medium](https://joseestevan.medium.com/)'
        st.markdown(medium, unsafe_allow_html=True) 
            
    st.subheader('By: José Estevan')

if __name__ == '__main__':
    main()




