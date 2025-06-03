# Import necessary libraries
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.preprocessing import MinMaxScaler

# Define the MCSDSS class
class MCSDSS:
    def __init__(self, shapefile=None, lat_lon=None):
        self.shapefile = shapefile
        self.lat_lon = lat_lon
        self.data = None
        self.criteria_weights = None
        self.criteria_data = None

    def load_data(self):
        """Load spatial data from a shapefile or latitude/longitude."""
        if self.shapefile:
            self.data = gpd.read_file(self.shapefile)
        elif self.lat_lon:
            self.data = self.create_geodataframe(self.lat_lon)
        else:
            raise ValueError("Either shapefile or latitude/longitude must be provided.")

    def create_geodataframe(self, lat_lon):
        """Create a GeoDataFrame from latitude and longitude."""
        geometry = [Point(lon, lat) for lon, lat in lat_lon]
        return gpd.GeoDataFrame(geometry=geometry)

    def set_criteria(self, criteria_data, weights):
        """Set criteria data and their respective weights."""
        self.criteria_data = criteria_data
        self.criteria_weights = weights

    def normalize_criteria(self):
        """Normalize criteria data for decision-making."""
        scaler = MinMaxScaler()
        self.normalized_data = scaler.fit_transform(self.criteria_data)

    def weighted_sum_model(self):
        """Apply the Weighted Sum Model for decision-making."""
        if self.normalized_data is None or self.criteria_weights is None:
            raise ValueError("Criteria data must be normalized and weights set before applying WSM.")
        
        scores = np.dot(self.normalized_data, self.criteria_weights)
        return scores

    def visualize_results(self, scores):
        """Visualize the results on a map."""
        self.data['scores'] = scores
        self.data.plot(column='scores', cmap='viridis', legend=True)
        plt.title('MCSDSS Results')
        plt.show()

    def run(self):
        """Run the MCSDSS application."""
        self.load_data()
        self.normalize_criteria()
        scores = self.weighted_sum_model()
        self.visualize_results(scores)

# Example usage
if __name__ == "__main__":
    # Define parameters
    shapefile_path = "path/to/your/shapefile.shp"
    lat_lon_data = [(longitude1, latitude1), (longitude2, latitude2)]  # Example coordinates

    # Initialize MCSDSS
    mcsdss = MCSDSS(shapefile=shapefile_path)

    # Load data
    mcsdss.load_data()

    # Set criteria data and weights (example data)
    criteria_data = np.array([[value1, value2], [value3, value4]])  # Replace with actual criteria data
    weights = np.array([0.5, 0.5])  # Example weights

    mcsdss.set_criteria(criteria_data, weights)

    # Run the MCSDSS application
    mcsdss.run()