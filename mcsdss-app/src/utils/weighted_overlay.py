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
        """Set weights for each criterion."""
        self.criteria_weights = weights
    
    def normalize_criteria(self):
        """Normalize criteria data using Min-Max scaling."""
        scaler = MinMaxScaler()
        for criterion, data in self.criteria_data.items():
            self.criteria_data[criterion] = scaler.fit_transform(data.values.reshape(-1, 1))
    
    def calculate_scores(self):
        """Calculate the overall score for each location based on criteria and weights."""
        scores = np.zeros(len(self.watershed_data))
        for criterion, weight in self.criteria_weights.items():
            scores += self.criteria_data[criterion].flatten() * weight
        self.watershed_data['score'] = scores
    
    def visualize_results(self):
        """Visualize the results on a map."""
        fig, ax = plt.subplots(figsize=(10, 10))
        self.watershed_data.plot(column='score', ax=ax, legend=True, cmap='viridis')
        plt.title('MCSDSS Results')
        plt.show()

# Example usage of the MCSDSS class
if __name__ == "__main__":
    # Initialize the MCSDSS application
    mcsdss = MCSDSS()

    # Load watershed data
    mcsdss.load_data(shapefile_path='path/to/watershed.shp')

    # Add criteria data (example data)
    mcsdss.add_criteria('Water Quality', pd.Series(np.random.rand(len(mcsdss.watershed_data))))
    mcsdss.add_criteria('Biodiversity', pd.Series(np.random.rand(len(mcsdss.watershed_data))))
    mcsdss.add_criteria('Land Use', pd.Series(np.random.rand(len(mcsdss.watershed_data))))

    # Set criteria weights
    mcsdss.set_criteria_weights({'Water Quality': 0.5, 'Biodiversity': 0.3, 'Land Use': 0.2})

    # Normalize criteria
    mcsdss.normalize_criteria()

    # Calculate scores
    mcsdss.calculate_scores()

    # Visualize results
    mcsdss.visualize_results()