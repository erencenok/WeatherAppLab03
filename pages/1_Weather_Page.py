import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title("Weather Forecast (Phase 2)")

city = st.text_input("Enter a city:", "Atlanta")
hours_to_show = st.slider("Hours to show", 6, 48, 24)

if st.button("Get Weather"):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_data = requests.get(geo_url).json()

    if "results" not in geo_data:
        st.error("City not found.")
    else:
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&hourly=temperature_2m"
        )

        weather_data = requests.get(weather_url).json()
        hours = weather_data["hourly"]["time"][:hours_to_show]
        temperatures = weather_data["hourly"]["temperature_2m"][:hours_to_show]

        plt.figure(figsize=(10, 5))
        plt.plot(hours, temperatures)
        plt.title(f"Next {hours_to_show} Hours Temperature in {city}")
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=45)

        st.pyplot(plt)

        st.subheader("Stats")
        st.write(f"Max Temp: {max(temperatures)}°C")
        st.write(f"Min Temp: {min(temperatures)}°C")
        st.write(f"Average Temp: {sum(temperatures)/len(temperatures):.2f}°C")
