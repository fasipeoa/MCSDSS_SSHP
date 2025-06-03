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
    
    def set_criteria_weights(self, weights):
        """Set weights for each criterion."""
        self.criteria_weights = weights
    
    def evaluate_criteria(self, criteria_data):
        """Evaluate criteria based on provided data."""
        for criterion, data in criteria_data.items():
            self.criteria_scores[criterion] = self.normalize_scores(data)
    
    def normalize_scores(self, scores):
        """Normalize scores using Min-Max scaling."""
        scaler = MinMaxScaler()
        return scaler.fit_transform(np.array(scores).reshape(-1, 1)).flatten()
    
    def calculate_overall_score(self):
        """Calculate the overall score based on criteria scores and weights."""
        overall_score = np.zeros(len(self.watershed_data))
        for criterion, score in self.criteria_scores.items():
            weight = self.criteria_weights.get(criterion, 0)
            overall_score += score * weight
        return overall_score
    
    def visualize_results(self, overall_score):
        """Visualize the results on a map."""
        self.watershed_data['Overall Score'] = overall_score
        self.watershed_data.plot(column='Overall Score', cmap='viridis', legend=True)
        plt.title('MCSDSS Overall Score')
        plt.show()

# Example usage
if __name__ == "__main__":
    # Initialize the MCSDSS application
    mcsdss = MCSDSS(watershed_data=None)
    
    # Load data (example shapefile path or lat/lon coordinates)
    mcsdss.load_data(shapefile_path='path/to/watershed.shp')
    # or
    # mcsdss.load_data(lat_lon=[(lon1, lat1), (lon2, lat2), ...])
    
    # Set criteria weights (example weights)
    criteria_weights = {
        'Water Quality': 0.4,
        'Biodiversity': 0.3,
        'Land Use': 0.3
    }
    mcsdss.set_criteria_weights(criteria_weights)
    
    # Evaluate criteria (example data)
    criteria_data = {
        'Water Quality': [85, 90, 78, 88],  # Example scores
        'Biodiversity': [70, 60, 80, 75],
        'Land Use': [60, 65, 70, 55]
    }
    mcsdss.evaluate_criteria(criteria_data)
    
    # Calculate overall score
    overall_score = mcsdss.calculate_overall_score()
    
    # Visualize results
    mcsdss.visualize_results(overall_score)