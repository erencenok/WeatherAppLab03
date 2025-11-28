import streamlit as st
from openai import OpenAI
import requests

st.title("AI Weather Broadcaster (OpenAI Version)")

# Load OpenAI key
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Inputs
city = st.text_input("City", "Chicago")
days = st.slider("How many days ahead?", 1, 7, 3)

# Get coordinates
def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    r = requests.get(url).json()
    if "results" not in r:
        return None, None
    lat = r["results"][0]["latitude"]
    lon = r["results"][0]["longitude"]
    return lat, lon

# Get weather
def get_weather(lat, lon, days):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_mean"
        f"&forecast_days={days}&timezone=auto"
    )
    return requests.get(url).json()

# Generate script with OpenAI
def make_script(city, days, weather_data):
    prompt = f"""
    You are a friendly TV weather broadcaster.

    Create a broadcast-style script for {city} for the next {days} days.
    Use this weather data:
    {weather_data}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text

if st.button("Generate Forecast Script"):
    try:
        lat, lon = get_coordinates(city)
        if lat is None:
            st.error("City not found.")
            st.stop()

        weather = get_weather(lat, lon, days)
        script = make_script(city, days, weather)

        st.subheader("📺 AI Weather Script")
        st.write(script)

    except Exception as e:
        st.error(f"Error: {e}")
