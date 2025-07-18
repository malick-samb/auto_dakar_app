import streamlit as st
import pandas as pd
import os
def load_(dataframe, title, key) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key):
      
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)
        
load_(pd.read_csv('data/location_auto.csv'), 'location_auto', '1')
load_(pd.read_csv('data/vente_auto.csv'), 'vente_auto', '2')
load_(pd.read_csv('data/vente_moto.csv'), 'vente_moto', '3')
