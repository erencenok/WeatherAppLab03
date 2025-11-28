import streamlit as st
import requests
import google.generativeai as genai

st.title("AI Weather Broadcaster (Phase 3)")

# Configuration should be done here
# Make sure GEMINI_API_KEY is correctly set in .streamlit/secrets.toml
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}. Check your secrets.")
    st.stop()


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

            # The slice might be incorrect if there aren't 24 hours of data,
            # but we'll stick to the original logic for now.
            temps = data["hourly"]["temperature_2m"][:24]

            prompt = f"""
            Create a fun weatherman broadcast script explaining the 24-hour temperature
            forecast for {city} {day} days from now.
            Temperatures: {temps}
            """

            # The standard model name is "gemini-pro"
            model = genai.GenerativeModel("gemini-pro") 
            response = model.generate_content(prompt)

            st.subheader("📢 Your AI Weather Script")
            st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
