import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"  # Adjust the URL if running on a different host/port

st.title("Predicting the Nature of Human Personality")

st.markdown("Please fill in the following details:")

# Input fields matching FastAPI model
Time_spent_Alone = st.slider("Time Spent Alone (in hours per day)", min_value=0, max_value=12, value=4)
Stage_fear = st.selectbox("Do you have stage fear?", options=[True, False])
Social_event_attendance = st.slider("Number of social events attended per month", min_value=0, max_value=10, value=5)
Going_outside = st.slider("Days you go outside in a week", min_value=0, max_value=7, value=3)
Drained_after_socializing = st.selectbox("Do you feel tired after socializing?", options=[True, False])
Friends_circle_size = st.slider("Number of friends in your circle", min_value=0, max_value=15, value=5)
Post_frequency = st.slider("How often do you post on social media per week?", min_value=0, max_value=10, value=4)

if st.button("Predict Personality Category"):
    input_data = {
        "Time_spent_Alone": Time_spent_Alone,
        "Stage_fear": Stage_fear,
        "Social_event_attendance": Social_event_attendance,
        "Going_outside": Going_outside,
        "Drained_after_socializing": Drained_after_socializing,
        "Friends_circle_size": Friends_circle_size,
        "Post_frequency": Post_frequency
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Personality Category: **{result}**")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the FastAPI server. Make sure it's running on port 8000.")
