import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌦️ Weather Dashboard")

city = st.text_input("Enter a city name:", "Atlanta")
days = st.slider("Forecast days:", 1, 7, 3)

geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geocode_url).json()

if "results" in geo_response:
    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    st.write(f"**Coordinates:** {lat}, {lon}")

    
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m&forecast_days={days}"
    weather_response = requests.get(weather_url).json()


    hourly = weather_response["hourly"]
    df = pd.DataFrame({
        "time": hourly["time"],
        "temperature": hourly["temperature_2m"],
    })

    st.subheader("Temperature Forecast")
    fig, ax = plt.subplots()
    ax.plot(df["time"], df["temperature"])
    ax.set_xticklabels(df["time"], rotation=45)
    st.pyplot(fig)

    st.write("### Stats")
    st.write(f"**Max Temp:** {df['temperature'].max()}°C")
    st.write(f"**Min Temp:** {df['temperature'].min()}°C")
    st.write(f"**Average Temp:** {df['temperature'].mean():.2f}°C")

else:
    st.error("City not found. Try another name.")
