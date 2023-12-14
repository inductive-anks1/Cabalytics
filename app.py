import streamlit as st
import pickle
import numpy as np
import datetime
import pandas as pd
import plotly.express as px
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
        current_date = datetime.datetime.today().date()
        date = st.date_input("Select the Date", current_date)

        # Extract year, month, day, and day of the week
        current_day = date.strftime('%A')

        current_month = date.month

        current_year = date.year

    with col2:
        selection_type = st.selectbox('Select Your Preferance', ['Entire Day', 'Manual Selection'])

    colD, colE = st.columns(2)

    if selection_type == 'Manual Selection':
        with colD:
            unique_hours = sorted(df['Current_Hour'].unique())
            current_hour = st.selectbox('Hour', unique_hours)

        with colE:
            time_frame_str = st.selectbox('Select The Time Frame', ['1', '2', '3'])
            time_frame = int(time_frame_str)

    results = []

    if st.button('Predict Price'):
        if selection_type == 'Entire Day':
            for current_hour in range(24):
                for current_min in range(0, 60, 10):
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

        if selection_type == 'Manual Selection':
            for current_hour in range(current_hour - time_frame, current_hour + time_frame + 1, 1):
                for current_min in range(0, 60, 10):
                    if 0 <= current_hour < 24:  # Ensure the hour is within the valid range
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
            if selection_type == "Entire Day":
                results_df = pd.DataFrame(results)
                top_10_cheapest = results_df.nsmallest(10, 'Cab_Price').reset_index(drop=True)

                min_price = results_df['Cab_Price'].min()
                min_time = results_df.loc[results_df['Cab_Price'].idxmin()]['Time']

                st.write("### Top 10 Cheapest Prices for the Entire Day 📉:")
                st.dataframe(top_10_cheapest)

                st.write(f"### The minimum price for this route is <span style='color: green; font-weight: bold;'>{min_price}</span> at <span style='color: green; font-weight: bold;'>{min_time}</span>", unsafe_allow_html=True)

            if selection_type == 'Manual Selection':
                results_df = pd.DataFrame(results)

                min_price = results_df['Cab_Price'].min()
                min_time = results_df.loc[results_df['Cab_Price'].idxmin()]['Time']

                st.write("### Predicted Results 📊:")
                st.dataframe(results_df)


                st.write(f"### The minimum price for this route is <span style='color: green; font-weight: bold;'>{min_price}</span> at <span style='color: green; font-weight: bold;'>{min_time}</span>", unsafe_allow_html=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.title('Analysis of Price and Route Time')

        fig = px.line(results_df, x='Time', y='Cab_Price', title='Cab Price Prediction Over Time',
                      labels={'Time': 'Time of Day', 'Cab_Price': 'Cab Price'})

        fig.update_traces(line=dict(color='#FC0080'))

        fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=4))
        st.plotly_chart(fig)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        fig_route = px.line(results_df, x='Time', y='Route Time', title='Route Time Prediction Over Time',
                            labels={'Time': 'Time of Day', 'Route Time': 'Route Time'})
        fig_route.update_traces(line=dict(color='#FC0080'))
        fig_route.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=4))

        st.plotly_chart(fig_route)