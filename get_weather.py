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

def search_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    current = fetch_weather(city)
    forecast = fetch_forecast(city)

    if "error" in current or current.get("cod") != 200:
        messagebox.showerror("Error", f"Failed to fetch data.\nReason: {current.get('message', 'Unknown error')}")
        return

    main = current["main"]
    wind = current["wind"]
    weather = current["weather"][0]

    temp = main["temp"]
    pressure = main["pressure"]
    humidity = main["humidity"]
    description = weather["description"].capitalize()
    wind_speed = wind["speed"]
    emoji = get_weather_emoji(description)

    text = (
        f"{emoji}  {city.title()}\n\n"
        f"🌡️ Temperature: {temp} °C\n"
        f"💨 Wind Speed: {wind_speed} m/s\n"
        f"💧 Humidity: {humidity}%\n"
        f"📈 Pressure: {pressure} hPa\n"
        f"🌤️ Weather: {description}\n"
        f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"📅 5-Day Forecast:\n"
    )

    for date, day_data in list(forecast.items())[:5]:
        emoji = get_weather_emoji(day_data["description"])
        text += f"{date}: {emoji} {day_data['description']} | {day_data['temp']}°C\n"

    result_label.config(text=text)
    save_weather_log(city, temp, pressure, humidity, description, wind_speed)

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    bg = "#1c1c1c" if dark_mode else "#D9EFFF"
    fg = "#FFFFFF" if dark_mode else "#1E3A8A"
    entry_bg = "#333333" if dark_mode else "#FFFFFF"
    result_bg = "#2a2a2a" if dark_mode else "#E3F2FD"
    btn_bg = "#4CAF50" if dark_mode else "#1E88E5"

    app.config(bg=bg)
    title_label.config(bg=bg, fg=fg)
    city_entry.config(bg=entry_bg, fg=fg, insertbackground=fg)
    search_button.config(bg=btn_bg, fg="white")
    theme_button.config(bg=btn_bg, fg="white", text="🌞 Light Mode" if dark_mode else "🌙 Dark Mode")
    result_label.config(bg=result_bg, fg=fg)
    footer_label.config(bg=bg, fg=fg)

# ---------- UI SETUP ----------
app = tk.Tk()
app.title("🌎 Weather Forecast App")
app.geometry("520x630")
app.resizable(False, False)

dark_mode = False
app.config(bg="#D9EFFF")

title_label = tk.Label(app, text="🌦️ Live Weather Forecast 🌦️", font=("Helvetica", 22, "bold"), bg="#D9EFFF", fg="#1E3A8A")
title_label.pack(pady=20)

city_entry = tk.Entry(app, font=("Helvetica", 16), width=25, justify="center", bd=2, relief="groove")
city_entry.pack(pady=15)

search_button = tk.Button(app, text="🔍 Search Weather", font=("Helvetica", 14, "bold"), bg="#1E88E5", fg="white", command=search_weather)
search_button.pack(pady=10)

theme_button = tk.Button(app, text="🌙 Dark Mode", font=("Helvetica", 12), command=toggle_theme)
theme_button.pack(pady=5)

result_label = tk.Label(app, text="", font=("Helvetica", 13), bg="#E3F2FD", fg="#0D47A1", justify="left", wraplength=480, padx=15, pady=20, bd=2, relief="groove")
result_label.pack(pady=20)

footer_label = tk.Label(app, text="📡 Powered by OpenWeatherMap API", font=("Helvetica", 10), bg="#D9EFFF", fg="#1E3A8A")
footer_label.pack(side="bottom", pady=10)

app.mainloop()
