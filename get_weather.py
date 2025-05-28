import streamlit as st
import requests
from datetime import datetime
import os

# Weather Description to Emoji Mapping
WEATHER_EMOJIS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "haze": "🌫️",
    "fog": "🌫️",
    "dust": "🌪️",
    "smoke": "💨",
    "sand": "🏜️",
}

# API Key (replace with your own key)
API_KEY = "850e42b8582ea97131bb274c1c3fbfe1"

def fetch_weather(city_name: str) -> dict:
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def fetch_forecast(city_name: str) -> dict:
    endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        daily = {}
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            if date not in daily:
                weather = entry["weather"][0]["description"].capitalize()
                temp = entry["main"]["temp"]
                daily[date] = {"temp": temp, "description": weather}
        return daily
    except requests.exceptions.RequestException:
        return {}

def get_weather_emoji(description: str) -> str:
    for key in WEATHER_EMOJIS:
        if key in description.lower():
            return WEATHER_EMOJIS[key]
    return "🌈"

def save_weather_log(city, temp, pressure, humidity, description, wind_speed):
    if not os.path.exists("weather_reports"):
        os.makedirs("weather_reports")
    with open("weather_reports/weather_log.txt", "a") as f:
        f.write(f"{datetime.now()} | {city.title()} | Temp: {temp}°C | Pressure: {pressure} hPa | Humidity: {humidity}% | Weather: {description} | Wind: {wind_speed} m/s\n")

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Weather Forecast", page_icon="🌎")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

bg_color = "#1c1c1c" if st.session_state.dark_mode else "#D9EFFF"
fg_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"

st.markdown(f"""
    <style>
        .reportview-container {{
            background-color: {bg_color};
            color: {fg_color};
        }}
        .sidebar .sidebar-content {{
            background-color: {bg_color};
        }}
    </style>
    """, unsafe_allow_html=True)

st.title("🌦️ Live Weather Forecast")

city = st.text_input("Enter city name", "")

col1, col2 = st.columns([3, 1])
search = col1.button("🔍 Search Weather")
theme_btn = col2.button("🌙 Toggle Theme" if not st.session_state.dark_mode else "🌞 Toggle Theme")

if theme_btn:
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.experimental_rerun()

if search and city:
    current = fetch_weather(city)
    forecast = fetch_forecast(city)

    if "error" in current or current.get("cod") != 200:
        st.error(f"Failed to fetch data. Reason: {current.get('message', 'Unknown error')}")
    else:
        main = current["main"]
        wind = current["wind"]
        weather = current["weather"][0]

        temp = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"].capitalize()
        wind_speed = wind["speed"]
        emoji = get_weather_emoji(description)

        st.markdown(f"## {emoji} {city.title()}")
        st.markdown(f"""
            - 🌡️ **Temperature:** {temp} °C  
            - 💨 **Wind Speed:** {wind_speed} m/s  
            - 💧 **Humidity:** {humidity}%  
            - 📈 **Pressure:** {pressure} hPa  
            - 🌤️ **Weather:** {description}  
            - 🕒 **Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)

        st.markdown("### 📅 5-Day Forecast:")
        for date, day_data in list(forecast.items())[:5]:
            f_emoji = get_weather_emoji(day_data["description"])
            st.write(f"{date}: {f_emoji} {day_data['description']} | {day_data['temp']}°C")

        save_weather_log(city, temp, pressure, humidity, description, wind_speed)
        st.success("✅ Weather data logged!")

st.markdown("---")
st.markdown("📡 Powered by [OpenWeatherMap](https://openweathermap.org/)")
