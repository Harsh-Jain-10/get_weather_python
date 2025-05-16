import requests
import tkinter as tk
from tkinter import messagebox
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

# API Key
API_KEY = "850e42b8582ea97131bb274c1c3fbfe1"  # Replace with your API key

def fetch_weather(city_name: str) -> dict:
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_weather_emoji(description: str) -> str:
    for key in WEATHER_EMOJIS:
        if key in description.lower():
            return WEATHER_EMOJIS[key]
    return "🌈"

def save_weather_log(city: str, temp: str, pressure: str, humidity: str, description: str, wind_speed: str) -> None:
    if not os.path.exists("weather_reports"):
        os.makedirs("weather_reports")
    filename = os.path.join("weather_reports", "weather_log.txt")
    with open(filename, "a") as file:
        file.write(f"{datetime.now()} | {city.title()} | Temp: {temp}°C | Pressure: {pressure} hPa | Humidity: {humidity}% | Weather: {description} | Wind: {wind_speed} m/s\n")

def search_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    weather_data = fetch_weather(city.strip())

    if "error" in weather_data or weather_data.get("cod") != 200:
        messagebox.showerror("Error", f"Failed to fetch weather data.\nReason: {weather_data.get('message', 'Unknown error')}")
        return

    main_data = weather_data.get("main", {})
    wind_data = weather_data.get("wind", {})
    weather = weather_data.get("weather", [{}])[0]

    temp = main_data.get("temp", 'N/A')
    pressure = main_data.get("pressure", 'N/A')
    humidity = main_data.get("humidity", 'N/A')
    description = weather.get("description", 'N/A').capitalize()
    wind_speed = wind_data.get("speed", 'N/A')
    emoji = get_weather_emoji(description)

    result_text = (
        f"{emoji}  {city.title()}\n\n"
        f"🌡️  Temperature: {temp} °C\n"
        f"💨  Wind Speed: {wind_speed} m/s\n"
        f"💧  Humidity: {humidity}%\n"
        f"📈  Pressure: {pressure} hPa\n"
        f"🌤️  Weather: {description}\n"
        f"🕒  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    result_label.config(text=result_text)

    save_weather_log(city, temp, pressure, humidity, description, wind_speed)

# ---------------- UI SETUP ---------------- #
app = tk.Tk()
app.title("🌎 Weather Forecast App")
app.geometry("480x550")
app.resizable(False, False)
app.configure(bg="#D9EFFF")  # Light Blue background

# Title
title_label = tk.Label(app, text="🌦️ Live Weather Forecast 🌦️", font=("Helvetica", 22, "bold"), bg="#D9EFFF", fg="#1E3A8A")
title_label.pack(pady=20)

# City Entry
city_entry = tk.Entry(app, font=("Helvetica", 16), width=25, justify="center", bd=2, relief="groove")
city_entry.pack(pady=15)

# Search Button
search_button = tk.Button(
    app,
    text="🔍 Search Weather",
    font=("Helvetica", 14, "bold"),
    bg="#1E88E5", 
    fg="white",
    activebackground="#1565C0",
    activeforeground="white",
    relief="raised",
    bd=4,
    padx=10,
    pady=5,
    command=search_weather
)
search_button.pack(pady=10)

# Result Display
result_label = tk.Label(
    app,
    text="",
    font=("Helvetica", 14),
    bg="#E3F2FD",  
    fg="#0D47A1",
    justify="center",
    wraplength=400,
    padx=15,
    pady=20,
    bd=2,
    relief="groove"
)
result_label.pack(pady=20)

# Footer
footer_label = tk.Label(app, text="📡 Powered by OpenWeatherMap API", font=("Helvetica", 10), bg="#D9EFFF", fg="#1E3A8A")
footer_label.pack(side="bottom", pady=10)

# Run App
app.mainloop()
