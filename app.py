import streamlit as st
import pickle
import numpy as np

pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

#Title
st.title('Cab Price Prediction')

#Cab Type
cab_type = st.selectbox('Cab Type', df['Cab_Type'].unique())

#Origin
pick_up = st.selectbox('Pick Up', df['Pick_Up'].unique())

#Destination
destination = st.selectbox('Destination', df['Destination'].unique())
