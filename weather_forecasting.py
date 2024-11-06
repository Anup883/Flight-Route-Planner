# weather_forecasting.py

import random

class WeatherForecast:
    def get_weather_data(self):
        # Simulated weather data affecting flight routes
        weather_data = {}
        airports = ['A', 'B', 'C', 'D', 'E']
        for i in range(len(airports)):
            for j in range(i + 1, len(airports)):
                if random.choice([True, False]):
                    weather_data[(airports[i], airports[j])] = random.randint(1, 5)  # Additional weight due to weather
        return weather_data