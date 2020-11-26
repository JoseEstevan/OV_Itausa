import streamlit as st
import os, glob
import codecs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import hyperlink

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)
def main():
    st.title('OverView')
    st.subheader('Ambev')
    file  = st.file_uploader('Escolha o dataset que deseja analisar (.csv)', type = 'csv')
    try:
        file.seek(0)
    except AttributeError:
        pass
    #file.seek(0)
    menu = ['Padrão','Pandas Profiling','Sweetviz','D-Tale','Sobre']
    
    if file is not None: 
        df = pd.read_csv(file)
        choice = st.sidebar.selectbox("Menu",menu)
        
        if choice == 'Padrão':
            
            if st.checkbox("DataSet"):
                number = st.slider('Escolha o numero de colunas que deseja ver', min_value=1, max_value=20)
                st.dataframe(df.head(number))
            if st.button("Colunas"):
                st.write(df.columns)

            if st.checkbox("Formato"):
                st.write(df.shape)
                data_dim = st.radio("Mostrar Por", ("Linhas", "Colunas"))
                if data_dim == 'Linhas':
                    st.text("Número de Linhas")
                    st.write(df.shape[0])
                elif data_dim == 'Colunas':
                    st.text("Número de Colunas")
                    st.write(df.shape[1])
            if st.checkbox("Selecionar Colunas"):
                all_columns = df.columns.tolist()
                selected_columns = st.multiselect('Selecione', all_columns)
                new_df = df[selected_columns]
                st.dataframe(new_df)

            if st.button("Tipos de Dados"):
                st.write(df.dtypes)
                
            if st.checkbox("Valores Faltantes"):
                st.write(df.isna().sum())
                st.write('Total(Colunas): {}'.format(df.isna().any().sum()))

            if st.checkbox("Sumário"):
                st.write(df.describe())

            st.subheader("Visualização De Dados")

            if st.checkbox("Correlação"):
                fig, ax = plt.subplots(figsize=(18,8))
                plt.xticks(rotation=45)
                sns.heatmap(df.corr(), cmap="Blues", annot=True)
                st.pyplot()
            
        
            if st.checkbox("Gráfico de Dispersão"):
                pd.set_option('plotting.backend', 'pandas_bokeh')
                all_columns = df.columns.tolist()
                x = st.selectbox("Eixo X", all_columns)
                y = st.selectbox('Eixo Y', all_columns)
                categoria = st.selectbox('Categoria', all_columns)
                if st.button("Plot"):
                    p_scatter = df.plot_bokeh.scatter(
                        x = x,
                        y = y,
                        category= categoria,)
                    st.write(p_scatter)

            if st.checkbox("Gráfico De Barras"):
                pd.set_option('plotting.backend', 'pandas_bokeh')
                all_columns_names = df.columns.tolist()
                primary_col = st.selectbox('Eixo X', all_columns_names)
                selected_column_names = st.multiselect('Eixo Y', all_columns_names)
                if st.button("Gerar"):
                    #st.text("Gerando Plot Para: {} and {}".format(primary_col, selected_column_names))
                    if selected_column_names:
                        vc_plot = df.groupby(primary_col)[selected_column_names].count()
                    else:
                        vc_plot = df.iloc[:, -1].value_counts()
                    st.write(vc_plot.plot(kind='bar'))
                    st.pyplot()
        
            if st.checkbox('Gráfico de Linhas'):
                pd.set_option('plotting.backend', 'pandas_bokeh')
                all_colunas = df.columns.tolist()
                xline = st.selectbox('Eixo X', all_colunas)
                yline = st.multiselect('Eixo Y', all_colunas)
                if st.button("Gerar"):
                    if yline:
                        p_line = df.groupby(xline)[yline].count()
                    else:
                        p_line = df.iloc[:, -1].value_counts()
                    st.write(p_line.plot(kind='line'))
                    st.pyplot()
        
            if st.checkbox('Gráfico de Área'):
                pd.set_option('plotting.backend', 'pandas_bokeh')
                todas_colunas = df.columns.tolist()
                x_area = st.selectbox('X', todas_colunas)
                y_area = st.selectbox('Y', todas_colunas)
                if st.button("Gerar"):
                    x_plot = df.plot_bokeh.area(
                        x = x_area,
                        y = y_area,
                        stacked = True,
                        legend="top_left"
                        )
                    st.write(x_plot)
        
            st.subheader("Features")

            if st.checkbox("Mostrar"):
                all_features = df.iloc[:, 0:-1]
                st.text('Nomes:: {}'.format(all_features.columns[0:-1]))
                st.dataframe(all_features.head(10))
        
        
        elif choice == 'Sweetviz':
            if st.button("Gerar Relatório"):
                st.success('Gerando...')
                report = sv.analyze(df)
                report.show_html()
                st_display("SWEETVIZ_REPORT.html")
        
        
        elif choice == 'Pandas Profiling':
            if st.button('Gerar Relatório'):
                try:
                    profiling = ProfileReport(df, title="Pandas Profiling", minimal=True)
                    st_profile_report(profiling)
                except AttributeError:
                    st.markdown('Feature em Manutenção')
                    pass

        elif choice == 'D-Tale':
            if st.button('Gerar Relatório'):
                st.text('Feature em Manutenção')
                #try:
                    #d = dtale.show(df, ignore_duplicate=True)
                    #d.open_browser()
                    #st.text(d._url)
                    #return (f"/dtale/main/{d._data_id}")
                #except AttributeError:
                    #st.markdown('Feature em Manutenção')
                    #pass

        elif choice == 'Sobre':
            st.header("Sobre o App")
            st.text('EDA(Exploratory Data Analysis) é uma abordagem à análise de conjuntos de dados,\nde modo a resumir suas características principais,\ncom o propósito de extrair informações relevantes. ')
            st.text('Criado com o objetivo de fornecer uma simples e rápida visualização sobre um dataset.')
            st.text('Feito para ser intuitivo e de fácil uso.')
            st.subheader('Redes Sociais')
            
            linkedin = '[LinkedIn](https://www.linkedin.com/in/joseestevan/)'
            st.markdown(linkedin, unsafe_allow_html=True) 
            
            github = '[GitHub](https://github.com/JoseEstevan)'
            st.markdown(github, unsafe_allow_html=True)  

            medium = '[Medium](https://joseestevan.medium.com/)'
            st.markdown(medium, unsafe_allow_html=True) 
               

        else:
            pass
            
    st.subheader('By: José Estevan')

if __name__ == '__main__':
    main()




