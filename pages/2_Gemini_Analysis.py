import streamlit as st
import requests
from google import genai

st.title("AI Weather Broadcaster (Phase 3)")

# Create client — NO configure()
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

city = st.text_input("City", "")
day = st.slider("How many days ahead?", 0, 7, 0)

if st.button("Generate Forecast Script"):

    try:
        # Get lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo = requests.get(geo_url).json()

        if "results" not in geo:
            st.error("City not found.")
            st.stop()

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        # Get weather
        w_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&daily=temperature_2m_max&timezone=auto"
        )
        weather = requests.get(w_url).json()

        forecast = weather["daily"]["temperature_2m_max"][day]

        # AI prompt
        prompt = f"""
        Create a short fun weather script.
        City: {city}
        Day: {day} days from now
        Max temp: {forecast}°C
        """

        # The correct new call in google-genai:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        st.subheader("Forecast Script")
        st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
