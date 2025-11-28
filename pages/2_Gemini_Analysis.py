from google import genai
import streamlit as st
import requests

st.title("AI Weather Broadcaster (Phase 3)")

client = genai.Client(api_key=api_key)

if st.button("Generate Forecast Script"):
    try:
        # weather_data = ... your API call
        
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
