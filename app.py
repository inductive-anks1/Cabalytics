import streamlit as st
import pickle
import numpy as np
import datetime
import pandas as pd
from PIL import Image

pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))
pipe_route = pickle.load(open('pipe_route.pkl', 'rb'))

st.set_page_config(layout="wide")

col1, col2, col3, col4, col5 = st.columns(5)


with col5:
    image = Image.open('Untitled.png')
    st.image(image)

col_1, col_2, col_3 = st.columns(3)

with col_1:
    st.title('CabAlytics')
    st.write('### by (Ankit, Noyonica, Surabhi)')

with col_2:
    st.write("")
    st.write("")
    st.write("")
    st.write('### Mentor - Prof. Siddharth')


colA, colB = st.columns(2)

st.write("")
st.write("")
st.write("")
st.write("")
st.write("")

with colA:
    # Title
    st.write('## Cab Price and Route Time Prediction :car:')

    # Cab Type
    cab_type = st.selectbox('Cab Type', df['Cab_Type'].unique())

    col1, col2 = st.columns(2)

    with col1:
        # Origin3
        pick_up = st.selectbox('Pick Up', df['Pick_Up'].unique())

    with col2:
        # Destination
        destination = st.selectbox('Destination', df['Destination'].unique())

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Select the Date", datetime.date(2023, 7, 6))

        # Extract year, month, day, and day of the week
        current_day = date.strftime('%A')

        current_month = date.month

        current_year = date.year

    with col2:
        unique_hours = sorted(df['Current_Hour'].unique())
        current_hour = st.selectbox('Hour', unique_hours)

    results = []

    if st.button('Predict Price'):
        for current_min in range(0, 61, 10):
            query = np.array([cab_type, pick_up, destination, current_day, current_hour,
                              current_min, current_month, current_year])

            query = query.reshape(1, 8)

            prediction = pipe.predict(query)[0]
            rounded_prediction = round(prediction, 2)

            prediction_route = pipe_route.predict(query)[0]
            rounded_prediction_route = round(prediction_route, 2)

            result_dict = {
                'Time': f'{current_hour:02d}:{current_min:02d}',
                'Cab_Price': rounded_prediction,
                'Route Time': rounded_prediction_route
            }

            results.append(result_dict)


with colB:
    # Displaying results in a DataFrame
    if results:
        results_df = pd.DataFrame(results)
        # Drop Current_Hour and Current_Minute columns
        results_df = results_df.drop(['Current_Hour', 'Current_Minute'], axis=1, errors='ignore')

        # Display the minimum values along with the message
        min_price = results_df['Cab_Price'].min()
        min_time = results_df.loc[results_df['Cab_Price'].idxmin()]['Time']

        st.write("### Predicted Results 📊:")
        st.dataframe(results_df)

        # Display the minimum price message

        st.write(f"### The minimum price for this route is <span style='color: green; font-weight: bold;'>{min_price}</span> at <span style='color: green; font-weight: bold;'>{min_time}</span>", unsafe_allow_html=True)

