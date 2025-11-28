import streamlit as st
import requests
import google.generativeai as genai

st.title("AI Weather Broadcaster (Phase 3)")

# configure API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

city = st.text_input("City", "")
day = st.slider("How many days ahead?", 0, 7, 0)

if st.button("Generate Forecast Script"):
    try:
        # Get lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo = requests.get(geo_url).json()

        if "results" not in geo:
            st.error("City not found")
            st.stop()

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        # Weather API
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days={day+1}&timezone=auto"
        )
        data = requests.get(weather_url).json()
        temps = data["hourly"]["temperature_2m"][:24]

        # Build prompt
        prompt = f"""
        You are a fun TV weatherman. Create a short broadcast script for the city {city},
        describing the next 24 hours of temperature data {day} days from now.
        Temperatures: {temps}
        """

        # USE CORRECT MODEL NAME
        model = genai.GenerativeModel("gemini-1.5-flash-001")
        response = model.generate_content(prompt)

        st.subheader("📢 Your AI Weather Script")
        st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
