import requests  # For making HTTP requests to the weather API
import json  # To handle the JSON response from the API
from datetime import datetime  # To format and display the current date and time

# Function to fetch and display weather information 
def get_weather(city_name, API_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}&units=metric"
    response = requests.get(url)  # Make a GET request to the API

    if response.status_code == 200:  # Check if the API call was successful
        data = response.json()  # Parse the JSON response
        
        # Extract key weather details from the API response
        main_data = data["main"]  
        weather_desc = data["weather"][0]["description"]  
        wind_speed = data["wind"]["speed"]  
        
        # Get and format the current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Display the weather forecast
        print(f"\nWeather forecast for {city_name.capitalize()} as of {current_time}:")
        print(f"Temperature: {main_data['temp']}°C")
        print(f"Pressure: {main_data['pressure']} hPa")
        print(f"Humidity: {main_data['humidity']}%")
        print(f"Weather Description: {weather_desc.capitalize()}")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        # Handle cases where the API call fails (e.g., invalid city name)
        print("City not found or unable to fetch the data.")

# Main Program
if __name__ == "__main__":
    API_key = "850e42b8582ea97131bb274c1c3fbfe1"  # Our OpenWeatherMap API key
    city_name = input("Enter city name: ")  
    get_weather(city_name, API_key)  # Fetch and display weather data
