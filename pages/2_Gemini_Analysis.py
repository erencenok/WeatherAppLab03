import streamlit as st
import requests
import google.generativeai as genai

st.title("AI Weather Broadcaster (Phase 3)")

# Configure API key using Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

city = st.text_input("City", "")
day = st.slider("How many days ahead?", 0, 7, 0)

if st.button("Generate Forecast Script"):
    try:
        # Step 1 — Get lat/lon
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo = requests.get(geo_url).json()

        if "results" not in geo:
            st.error("City not found.")
            st.stop()

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        # Step 2 — Get forecast
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&daily=temperature_2m_max&timezone=auto"
        )
        weather = requests.get(weather_url).json()

        forecast = weather["daily"]["temperature_2m_max"][day]

        # Step 3 — Build prompt
        prompt = (
            f"Create a short, fun weather broadcast about {city}, "
            f"{day} days from now. The high temperature will be {forecast}°C."
        )

        # Step 4 — Gemini call
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        st.subheader("AI Weather Script")
        st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
