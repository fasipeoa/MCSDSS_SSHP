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
        if shapefile_path:
            self.watershed_data = gpd.read_file(shapefile_path)
        elif lat_lon:
            # Create a GeoDataFrame from latitude and longitude
            self.watershed_data = gpd.GeoDataFrame(
                {'geometry': [Point(lon, lat) for lon, lat in lat_lon]},
                crs="EPSG:4326"
            )
        else:
            raise ValueError("Either shapefile_path or lat_lon must be provided.")

    def set_criteria_weights(self, weights):
        self.criteria_weights = weights

    def evaluate_criteria(self, criteria_functions):
        for criterion, function in criteria_functions.items():
            self.criteria_scores[criterion] = function(self.watershed_data)

    def normalize_scores(self):
        scaler = MinMaxScaler()
        for criterion, scores in self.criteria_scores.items():
            self.criteria_scores[criterion] = scaler.fit_transform(scores.values.reshape(-1, 1))

    def aggregate_scores(self):
        self.watershed_data['final_score'] = 0
        for criterion, weight in self.criteria_weights.items():
            self.watershed_data['final_score'] += self.criteria_scores[criterion] * weight

    def visualize_results(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        self.watershed_data.plot(column='final_score', ax=ax, legend=True,
                                 legend_kwds={'label': "Final Score", 'orientation': "horizontal"})
        plt.title("MCSDSS Results")
        plt.show()

# Define criteria functions
def water_quality(data):
    # Placeholder for water quality evaluation logic
    return data['water_quality_index']

def land_use(data):
    # Placeholder for land use evaluation logic
    return data['land_use_index']

def biodiversity(data):
    # Placeholder for biodiversity evaluation logic
    return data['biodiversity_index']

# Example usage
if __name__ == "__main__":
    # Initialize MCSDSS
    mcsdss = MCSDSS(None)

    # Load watershed data
    mcsdss.load_data(shapefile_path='path/to/watershed.shp')

    # Set criteria weights (example)
    mcsdss.set_criteria_weights({
        'water_quality': 0.4,
        'land_use': 0.3,
        'biodiversity': 0.3
    })

    # Evaluate criteria
    criteria_functions = {
        'water_quality': water_quality,
        'land_use': land_use,
        'biodiversity': biodiversity
    }
    mcsdss.evaluate_criteria(criteria_functions)

    # Normalize scores
    mcsdss.normalize_scores()

    # Aggregate scores
    mcsdss.aggregate_scores()

    # Visualize results
    mcsdss.visualize_results()