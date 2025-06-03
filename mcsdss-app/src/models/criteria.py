# Import necessary libraries
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.preprocessing import MinMaxScaler

# Define the MCSDSS class
class MCSDSS:
    def __init__(self, criteria_weights, criteria_functions):
        self.criteria_weights = criteria_weights  # Dictionary of criteria weights
        self.criteria_functions = criteria_functions  # Dictionary of criteria functions
        self.data = None
        self.results = None

    def load_data(self, shapefile_path=None, lat_lon=None):
        """Load spatial data from a shapefile or latitude/longitude."""
        if shapefile_path:
            self.data = gpd.read_file(shapefile_path)
        elif lat_lon:
            self.data = self.create_geodataframe(lat_lon)
        else:
            raise ValueError("Either shapefile_path or lat_lon must be provided.")

    def create_geodataframe(self, lat_lon):
        """Create a GeoDataFrame from latitude and longitude."""
        geometry = [Point(lon, lat) for lon, lat in lat_lon]
        return gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")

    def preprocess_data(self):
        """Preprocess the data for analysis."""
        # Normalize criteria data
        for criterion in self.criteria_functions.keys():
            self.data[criterion] = self.criteria_functions[criterion](self.data)

    def apply_weights(self):
        """Apply weights to the criteria and calculate the overall score."""
        self.data['score'] = 0
        for criterion, weight in self.criteria_weights.items():
            self.data['score'] += self.data[criterion] * weight

    def analyze(self):
        """Run the analysis and generate results."""
        self.preprocess_data()
        self.apply_weights()
        self.results = self.data.sort_values(by='score', ascending=False)

    def visualize_results(self):
        """Visualize the results on a map."""
        fig, ax = plt.subplots(figsize=(10, 10))
        self.data.plot(column='score', ax=ax, legend=True,
                       legend_kwds={'label': "Score by Criteria",
                                    'orientation': "horizontal"})
        plt.title("MCSDSS Results")
        plt.show()

# Define criteria functions
def normalize_criterion(data, criterion):
    """Normalize a specific criterion."""
    scaler = MinMaxScaler()
    return scaler.fit_transform(data[[criterion]]).flatten()

# Example usage
if __name__ == "__main__":
    # Define criteria weights and functions
    criteria_weights = {
        'water_quality': 0.4,
        'biodiversity': 0.3,
        'land_use': 0.2,
        'proximity_to_water': 0.1
    }

    criteria_functions = {
        'water_quality': lambda data: normalize_criterion(data, 'water_quality'),
        'biodiversity': lambda data: normalize_criterion(data, 'biodiversity'),
        'land_use': lambda data: normalize_criterion(data, 'land_use'),
        'proximity_to_water': lambda data: normalize_criterion(data, 'proximity_to_water')
    }

    # Initialize MCSDSS
    mcsdss = MCSDSS(criteria_weights, criteria_functions)

    # Load data (example shapefile path or lat/lon)
    mcsdss.load_data(shapefile_path='path/to/shapefile.shp')
    # OR
    # mcsdss.load_data(lat_lon=[(lon1, lat1), (lon2, lat2), ...])

    # Analyze and visualize results
    mcsdss.analyze()
    mcsdss.visualize_results()