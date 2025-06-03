# Import necessary libraries
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.preprocessing import MinMaxScaler

# Define the MCSDSS class
class MCSDSS:
    def __init__(self, watershed_data):
        self.watershed_data = watershed_data
        self.criteria_weights = {}
        self.criteria_scores = {}
    
    def load_data(self, shapefile_path=None, lat_lon=None):
        """Load watershed data from a shapefile or latitude/longitude."""
        if shapefile_path:
            self.watershed_data = gpd.read_file(shapefile_path)
        elif lat_lon:
            self.watershed_data = self.create_geodataframe(lat_lon)
        else:
            raise ValueError("Either shapefile_path or lat_lon must be provided.")
    
    def create_geodataframe(self, lat_lon):
        """Create a GeoDataFrame from latitude and longitude."""
        geometry = [Point(lon, lat) for lon, lat in lat_lon]
        return gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")
    
    def set_criteria_weights(self, criteria_weights):
        """Set weights for each criterion."""
        self.criteria_weights = criteria_weights
    
    def evaluate_criteria(self, criteria_functions):
        """Evaluate criteria using provided functions."""
        for criterion, function in criteria_functions.items():
            self.criteria_scores[criterion] = function(self.watershed_data)
    
    def normalize_scores(self):
        """Normalize scores to a common scale."""
        scaler = MinMaxScaler()
        for criterion, scores in self.criteria_scores.items():
            self.criteria_scores[criterion] = scaler.fit_transform(scores.values.reshape(-1, 1))
    
    def aggregate_scores(self):
        """Aggregate scores based on weights."""
        self.watershed_data['final_score'] = 0
        for criterion, weight in self.criteria_weights.items():
            self.watershed_data['final_score'] += self.criteria_scores[criterion] * weight
    
    def visualize_results(self):
        """Visualize the final scores on a map."""
        fig, ax = plt.subplots(figsize=(10, 10))
        self.watershed_data.plot(column='final_score', ax=ax, legend=True,
                                 legend_kwds={'label': "Final Score",
                                              'orientation': "horizontal"})
        plt.title("MCSDSS Results")
        plt.show()

# Example usage
if __name__ == "__main__":
    # Initialize the MCSDSS application
    mcsdss = MCSDSS(None)
    
    # Load data (example shapefile path or lat/lon coordinates)
    mcsdss.load_data(shapefile_path='path/to/watershed.shp')
    # or
    # mcsdss.load_data(lat_lon=[(lon1, lat1), (lon2, lat2), ...])
    
    # Set criteria weights (example)
    criteria_weights = {
        'water_quality': 0.4,
        'biodiversity': 0.3,
        'land_use': 0.3
    }
    mcsdss.set_criteria_weights(criteria_weights)
    
    # Define criteria evaluation functions (example)
    def water_quality(data):
        return data['water_quality_index']  # Replace with actual column name
    
    def biodiversity(data):
        return data['biodiversity_index']  # Replace with actual column name
    
    def land_use(data):
        return data['land_use_index']  # Replace with actual column name
    
    criteria_functions = {
        'water_quality': water_quality,
        'biodiversity': biodiversity,
        'land_use': land_use
    }
    
    # Evaluate criteria
    mcsdss.evaluate_criteria(criteria_functions)
    
    # Normalize scores
    mcsdss.normalize_scores()
    
    # Aggregate scores
    mcsdss.aggregate_scores()
    
    # Visualize results
    mcsdss.visualize_results()