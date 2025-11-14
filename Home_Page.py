import streamlit as st

st.set_page_config(
    page_title="Lab03",
    page_icon="🌦️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Title of App
st.title("Web Development Lab03")

# Assignment Data
# TODO: Replace TEAM NUMBER, SECTION, and MEMBER NAMES
st.header("CS 1301 — Web Development")
st.subheader("Team 12 — Section E")
st.subheader("Team Members: Eren Cetinok, Michael Driscoll")

st.write("---")

# Introduction + Required Page Descriptions
st.markdown("""
Welcome to our Streamlit Web Development Lab03 project!  
Use the sidebar on the left to navigate between the different pages.

---

### 📄 Pages in This Application

#### **1. Home Page**
Overview of the project and navigation to all other pages.

#### **2. Weather Page**
Displays real-time weather data using an external API, with interactive graphs and analysis.

#### **3. Gemini Analysis Page**
Uses the Google Gemini LLM to analyze weather trends and generate explanatory or creative text.

#### **4. Gemini Chatbot Page**
An intelligent chatbot that understands weather data and remembers the conversation context.

---

### 🌟 Feel free to explore!
""")
