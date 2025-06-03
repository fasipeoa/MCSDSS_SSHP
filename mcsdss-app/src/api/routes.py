# Import necessary libraries
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.preprocessing import MinMaxScaler

# Define the MCSDSS class
class MCSDSS:
    def __init__(self, watershed_data, criteria_weights):
        """
        Initialize the MCSDSS application.
        
        :param watershed_data: Path to the shapefile or a DataFrame with latitude/longitude
        :param criteria_weights: Dictionary with criteria names and their corresponding weights
        """
        self.watershed_data = self.load_data(watershed_data)
        self.criteria_weights = criteria_weights
        self.criteria_scores = None

    def load_data(self, watershed_data):
        """
        Load watershed data from a shapefile or latitude/longitude parameters.
        
        :param watershed_data: Path to the shapefile or DataFrame
        :return: GeoDataFrame
        """
        if isinstance(watershed_data, str):
            return gpd.read_file(watershed_data)
        elif isinstance(watershed_data, pd.DataFrame):
            geometry = [Point(xy) for xy in zip(watershed_data.longitude, watershed_data.latitude)]
            return gpd.GeoDataFrame(watershed_data, geometry=geometry)
        else:
            raise ValueError("Invalid watershed data format. Provide a shapefile path or DataFrame.")

    def normalize_criteria(self):
        """
        Normalize the criteria scores to a common scale.
        """
        scaler = MinMaxScaler()
        self.criteria_scores = scaler.fit_transform(self.watershed_data[self.criteria_weights.keys()])

    def calculate_weighted_scores(self):
        """
        Calculate the weighted scores based on criteria weights.
        """
        weighted_scores = np.dot(self.criteria_scores, np.array(list(self.criteria_weights.values())))
        self.watershed_data['weighted_score'] = weighted_scores

    def analyze(self):
        """
        Perform the analysis and generate results.
        """
        self.normalize_criteria()
        self.calculate_weighted_scores()
        return self.watershed_data[['geometry', 'weighted_score']]

    def visualize_results(self):
        """
        Visualize the results of the analysis.
        """
        self.watershed_data.plot(column='weighted_score', cmap='viridis', legend=True)
        plt.title('MCSDSS Weighted Scores')
        plt.show()

# Example usage
if __name__ == "__main__":
    # Define criteria weights (example)
    criteria_weights = {
        'water_quality': 0.4,
        'land_use': 0.3,
        'biodiversity': 0.3
    }

    # Load watershed data (example shapefile path)
    watershed_data_path = 'path/to/watershed_shapefile.shp'

    # Create an instance of MCSDSS
    mcsdss = MCSDSS(watershed_data=watershed_data_path, criteria_weights=criteria_weights)

    # Analyze the watershed data
    results = mcsdss.analyze()

    # Visualize the results
    mcsdss.visualize_results()