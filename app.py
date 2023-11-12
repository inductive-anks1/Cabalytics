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

#Current Day
current_day = st.selectbox('Day', df['Current Day'].unique())

#Hour
unique_hours = sorted(df['Current_Hour'].unique())
current_hour = st.selectbox('Hour', unique_hours)

#Minute
current_min = st.number_input('Current Minute')

#Month
current_month = st.selectbox('Month', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])

#Year
current_year = st.number_input('Current Year')


if st.button('Predict Price'):
    pass