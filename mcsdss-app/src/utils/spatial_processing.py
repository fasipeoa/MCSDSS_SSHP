# Import necessary libraries
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.preprocessing import MinMaxScaler

# Define the MCSDSS class
class MCSDSS:
    def __init__(self, watershed_data, criteria_weights):
        self.watershed_data = watershed_data  # GeoDataFrame
        self.criteria_weights = criteria_weights  # Dictionary of criteria and their weights
        self.scaled_data = None

    def load_data(self, shapefile_path=None, lat_lon=None):
        """Load watershed data from a shapefile or latitude/longitude."""
        if shapefile_path:
            self.watershed_data = gpd.read_file(shapefile_path)
        elif lat_lon:
            # Create a GeoDataFrame from latitude and longitude
            self.watershed_data = gpd.GeoDataFrame(
                lat_lon, 
                geometry=gpd.points_from_xy(lat_lon['longitude'], lat_lon['latitude']),
                crs="EPSG:4326"
            )
        else:
            raise ValueError("Either shapefile_path or lat_lon must be provided.")

    def normalize_criteria(self):
        """Normalize the criteria data using Min-Max scaling."""
        scaler = MinMaxScaler()
        self.scaled_data = pd.DataFrame(scaler.fit_transform(self.watershed_data.select_dtypes(include=[np.number])),
                                         columns=self.watershed_data.select_dtypes(include=[np.number]).columns)

    def apply_weights(self):
        """Apply weights to the normalized criteria."""
        for criterion, weight in self.criteria_weights.items():
            if criterion in self.scaled_data.columns:
                self.scaled_data[criterion] *= weight

    def calculate_scores(self):
        """Calculate the final scores for each watershed."""
        self.watershed_data['score'] = self.scaled_data.sum(axis=1)

    def visualize_results(self):
        """Visualize the results on a map."""
        fig, ax = plt.subplots(figsize=(10, 10))
        self.watershed_data.plot(column='score', ax=ax, legend=True,
                                 legend_kwds={'label': "Score by Watershed",
                                              'orientation': "horizontal"})
        plt.title("MCSDSS Results")
        plt.show()

    def run_analysis(self):
        """Run the complete analysis."""
        self.normalize_criteria()
        self.apply_weights()
        self.calculate_scores()
        self.visualize_results()

# Example usage
if __name__ == "__main__":
    # Define criteria weights (example)
    criteria_weights = {
        'water_quality': 0.4,
        'biodiversity': 0.3,
        'land_use': 0.3
    }

    # Initialize MCSDSS
    mcsdss = MCSDSS(watershed_data=None, criteria_weights=criteria_weights)

    # Load data (example with shapefile)
    mcsdss.load_data(shapefile_path='path/to/watershed_shapefile.shp')

    # Run the analysis
    mcsdss.run_analysis()