# Import necessary libraries
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.preprocessing import MinMaxScaler

# Define the MCSDSS class
class MCSDSS:
    def __init__(self, watershed_data=None):
        self.watershed_data = watershed_data
        self.criteria_weights = {}
        self.criteria_data = {}
    
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
    
    def add_criteria(self, criteria_name, data):
        """Add criteria data to the MCSDSS."""
        self.criteria_data[criteria_name] = data
    
    def set_criteria_weights(self, weights):
        """Set weights for each criteria."""
        self.criteria_weights = weights
    
    def normalize_criteria(self):
        """Normalize criteria data for comparison."""
        scaler = MinMaxScaler()
        for criteria_name, data in self.criteria_data.items():
            self.criteria_data[criteria_name] = scaler.fit_transform(data.values.reshape(-1, 1))
    
    def evaluate_alternatives(self):
        """Evaluate alternatives based on criteria and weights."""
        scores = {}
        for criteria_name, data in self.criteria_data.items():
            weight = self.criteria_weights.get(criteria_name, 0)
            scores[criteria_name] = data * weight
        
        # Aggregate scores
        total_scores = np.sum(list(scores.values()), axis=0)
        return total_scores
    
    def visualize_results(self, scores):
        """Visualize the results of the evaluation."""
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(scores)), scores)
        plt.title('MCSDSS Evaluation Scores')
        plt.xlabel('Alternatives')
        plt.ylabel('Scores')
        plt.xticks(range(len(scores)), [f'Alt {i+1}' for i in range(len(scores))])
        plt.show()

# Example usage
if __name__ == "__main__":
    # Initialize the MCSDSS
    mcsdss = MCSDSS()

    # Load watershed data (example shapefile path)
    mcsdss.load_data(shapefile_path='path/to/watershed.shp')

    # Add criteria data (example data)
    mcsdss.add_criteria('Water Quality', pd.Series([80, 70, 90, 60]))
    mcsdss.add_criteria('Biodiversity', pd.Series([60, 80, 70, 90]))
    mcsdss.add_criteria('Accessibility', pd.Series([70, 60, 80, 90]))

    # Set criteria weights
    mcsdss.set_criteria_weights({'Water Quality': 0.5, 'Biodiversity': 0.3, 'Accessibility': 0.2})

    # Normalize criteria
    mcsdss.normalize_criteria()

    # Evaluate alternatives
    scores = mcsdss.evaluate_alternatives()

    # Visualize results
    mcsdss.visualize_results(scores)