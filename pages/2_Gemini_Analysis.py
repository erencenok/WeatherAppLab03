import streamlit as st
import requests
import google.generativeai as genai

st.title("AI Weather Broadcaster (Phase 3)")

# Correct API key setup for google-generativeai==0.8.3
genai.api_key = st.secrets["GEMINI_API_KEY"]

city = st.text_input("City")
day = st.slider("How many days ahead?", 0, 7, 0)

if st.button("Generate Forecast Script"):
    try:
        # 1. Get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo = requests.get(geo_url).json()

        if "results" not in geo:
            st.error("City not found.")
            st.stop()

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        # 2. Get weather
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&hourly=temperature_2m&forecast_days={day+1}&timezone=auto"
        )
        data = requests.get(weather_url).json()
        temps = data["hourly"]["temperature_2m"][:24]

        # 3. Gemini call
        prompt = f"""
        Create a fun weather broadcaster script for {city}, {day} days from now.
        Temperatures (24 hours): {temps}
        """

        model = genai.GenerativeModel("gemini-pro")  # 0.8.3 uses "gemini-pro"
        response = model.generate_content(prompt)

        st.subheader("📢 Your AI Weather Script")
        st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
