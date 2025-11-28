from google import genai
import streamlit as st
import requests

st.title("AI Weather Broadcaster (Phase 3)")

# --- FIX: Define your API key ---
api_key = st.secrets["GOOGLE_API_KEY"]

# Create Gemini client
client = genai.Client(api_key=api_key)

# Inputs
city = st.text_input("City", "Chicago")
day = st.slider("How many days ahead?", 1, 7, 4)

if st.button("Generate Forecast Script"):
    try:
        # (Your weather API fetch goes here)
        weather_data = "Weather data goes here"

        prompt = f"""
        Generate a friendly weather broadcast for {city} for the next {day} days.
        Here is the raw forecast data:
        {weather_data}
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        forecast_text = response.text  
        st.success(forecast_text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
