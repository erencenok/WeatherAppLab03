import streamlit as st
import requests
import google.generativeai as genai

st.title("AI Weather Broadcaster (Phase 3)")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

city = st.text_input("City", "")
day = st.slider("How many days ahead?", 0, 7, 0)

if st.button("Generate Forecast Script"):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo = requests.get(geo_url).json()

        if "results" not in geo:
            st.error("City not found")
        else:
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days={day+1}&timezone=auto"
            )
            data = requests.get(weather_url).json()

            temps = data["hourly"]["temperature_2m"][:24]

            prompt = f"""
            Create a fun weatherman broadcast script explaining the 24-hour temperature
            forecast for {city} {day} days from now.
            Temperatures: {temps}
            """

            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)

            st.subheader("📢 Your AI Weather Script")
            st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
