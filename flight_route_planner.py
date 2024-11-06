# flight_route_planner.py

import networkx as nx
import numpy as np
from weather_forecasting import WeatherForecast
from air_traffic_management import AirTrafficManagement

class FlightRoutePlanner:
    def __init__(self):
        self.graph = nx.Graph()
        self.weather_forecast = WeatherForecast()
        self.air_traffic_management = AirTrafficManagement()
        self.create_graph()

    def create_graph(self):
        # Define airports as nodes
        airports = [
            'Indira Gandhi International Airport (DEL) - New Delhi',
            'Chaudhary Charan Singh Airport (LKO) - Lucknow',
            'Srinagar International Airport (SXR) - Srinagar',
            'Jaipur International Airport (JAI) - Jaipur',
            'Goa International Airport (GOI) - Dabolim, Goa',
            'Pune International Airport (PNQ) - Pune',
            'Chennai International Airport (MAA) - Chennai',
            'Rajiv Gandhi International Airport (HYD) - Hyderabad',
            'Biju Patnaik International Airport (BBI) - Bhubaneswar',
            'Bagdogra Airport (IXB) - Siliguri'
        ]
        for airport in airports:
            self.graph.add_node(airport)

        # Add edges with random weights between all pairs of airports
        for i, airport1 in enumerate(airports):
            for j, airport2 in enumerate(airports):
                if i < j:  # Avoid duplicating edges
                    weight = np.random.randint(100, 500)
                    self.graph.add_edge(airport1, airport2, weight=weight)

    def get_optimal_route(self, start, end):
        # Retrieve weather data to adjust weights based on conditions
        weather_conditions = self.weather_forecast.get_weather_data()
        self.adjust_weights(weather_conditions)

        # Use Dijkstra's algorithm to find the optimal route
        optimal_route = nx.dijkstra_path(self.graph, source=start, target=end, weight='weight')
        return optimal_route

    def adjust_weights(self, weather_conditions):
        # Adjust graph weights based on weather data
        for (u, v, wt) in self.graph.edges(data=True):
            if weather_conditions.get((u, v)):
                wt['weight'] += weather_conditions[(u, v)]
