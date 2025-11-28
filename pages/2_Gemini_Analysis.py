import streamlit as st
from openai import OpenAI
import requests

st.title("AI Weather Broadcaster (Phase 3)")

# Load OpenAI key from secrets
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# User inputs
city = st.text_input("City", "Chicago")
day = st.slider("How many days ahead?", 1, 7, 4)

if st.button("Generate Forecast Script"):
    try:
        # Replace with real weather API call
        weather_data = "Sample weather data here"

        prompt = f"""
        Create a friendly, TV-style weather broadcast for {city}
        for the next {day} days. Use this weather data:
        {weather_data}
        """

        # OpenAI generation
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        forecast = response.output_text
        st.success(forecast)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
