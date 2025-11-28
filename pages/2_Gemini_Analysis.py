import streamlit as st
from google import genai

# Load your Gemini API key from Streamlit secrets:
api_key = st.secrets["GEMINI_API_KEY"]

# Create the Gemini client
client = genai.Client(api_key=api_key)

st.title("Weather Analysis with Google Gemini")

# User inputs
city = st.text_input("City", "Atlanta")
day = st.slider("Days ahead (1–7)", 1, 7, 3)

# Example weather data (replace with real API)
weather_data = {
    "temperature": "75°F",
    "rain": "10%",
    "wind": "5 mph",
}

if st.button("Generate Forecast Script"):
    try:
        prompt = f"""
        You are a TV weatherman. Create a fun, conversational weather
        forecast for {city} for the next {day} days using this data:
        {weather_data}
        """

        # Correct Gemini API call
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        st.subheader("📺 Your Weatherman Script:")
        st.write(response.text)

    except Exception as e:
        st.error(f"ERROR: {e}")
