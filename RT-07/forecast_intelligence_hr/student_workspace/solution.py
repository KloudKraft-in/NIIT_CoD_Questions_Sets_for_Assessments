from enum import Enum
from typing import Dict, Any, Optional
import sys

# Complete the 'WeatherService' class below.
#
# Processes weather queries using a dynamic Enum.

class WeatherService:
    # Class-level variable to store the dynamic Enum
    WeatherData: Optional[Enum] = None

    @staticmethod
    def initialize_data(data: Dict[str, Dict[str, Any]]) -> None:
        """Dynamically creates an Enum from city data."""
        # Implementation here
        pass

    @staticmethod
    def get_temperature(city: str) -> str:
        """Fetches temperature for a given city from the dynamic Enum.
        Requirement:
        - If city not in Data, raise ValueError("Invalid city name <city>")
        - Convert temperature to float and validate range [-25, 122].
        - If out of range or invalid format, raise ValueError("Temperature <val> is out of range")
        - Return string: "The temperature for <city> is <int(temp)>"
        """
        # Implementation here
        return ""

    @staticmethod
    def get_forecast(city: str) -> str:
        """Fetches forecast for a given city from the dynamic Enum.
        Requirement:
        - If city not in Data, raise ValueError("Invalid city name <city>")
        - Return string: "The forecast for <city> is <forecast>"
        """
        # Implementation here
        return ""







#NOTE : Don't  modify below code.

def process_weather_queries():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
        
    line_idx = 0
    n_cities = int(input_data[line_idx].strip())
    line_idx += 1
    city_map = {}
    
    for _ in range(n_cities):
        if line_idx >= len(input_data): break
        line = input_data[line_idx].strip().split(",")
        city = line[0].strip()
        temp = line[1].strip()
        forecast = line[2].strip()
        city_map[city] = {"temp": temp, "forecast": forecast}
        line_idx += 1
    
    WeatherService.initialize_data(city_map)

    if line_idx >= len(input_data): return
    n_queries = int(input_data[line_idx].strip())
    line_idx += 1
    
    for _ in range(n_queries):
        if line_idx >= len(input_data): break
        query = input_data[line_idx].strip().split(",")
        line_idx += 1
        if len(query) < 2: continue
        city = query[0].strip()
        q_type = query[1].strip()
        
        try:
            if q_type == "temperature":
                print(WeatherService.get_temperature(city))
            elif q_type == "forecast":
                print(WeatherService.get_forecast(city))
        except ValueError as e:
            # Catching validation errors and printing in 'Error: <msg>' format
            # This ensures the script doesn't crash during evaluation.
            print(f"Error: {e}")

if __name__ == '__main__':
    process_weather_queries()
