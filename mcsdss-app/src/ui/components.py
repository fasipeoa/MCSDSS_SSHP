# Import necessary libraries
import geopandas as gpd
import numpy as np
import pandas as pd
import folium
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
            self.watershed_data = self.create_geodataframe(lat_lon)
        else:
            raise ValueError("Either shapefile_path or lat_lon must be provided.")
    
    def create_geodataframe(self, lat_lon):
        # Create a GeoDataFrame from latitude and longitude
        geometry = [Point(lon, lat) for lon, lat in lat_lon]
        return gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")
    
    def define_criteria(self, criteria):
        # Define criteria and their weights
        for criterion, weight in criteria.items():
            self.criteria_weights[criterion] = weight
    
    def score_criteria(self, scoring_functions):
        # Score each criterion using provided scoring functions
        for criterion, func in scoring_functions.items():
            self.criteria_scores[criterion] = func(self.watershed_data)
    
    def normalize_scores(self):
        # Normalize scores using Min-Max scaling
        scaler = MinMaxScaler()
        for criterion, scores in self.criteria_scores.items():
            self.criteria_scores[criterion] = scaler.fit_transform(scores.values.reshape(-1, 1))
    
    def aggregate_scores(self):
        # Aggregate scores based on defined weights
        self.watershed_data['final_score'] = 0
        for criterion, weight in self.criteria_weights.items():
            self.watershed_data['final_score'] += self.criteria_scores[criterion] * weight
    
    def visualize_results(self):
        # Visualize the results on a map
        m = folium.Map(location=[self.watershed_data.geometry.y.mean(), self.watershed_data.geometry.x.mean()], zoom_start=10)
        folium.Choropleth(
            geo_data=self.watershed_data,
            data=self.watershed_data['final_score'],
            key_on='feature.properties.final_score',
            fill_color='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Final Score'
        ).add_to(m)
        return m

# Example usage
if __name__ == "__main__":
    # Initialize MCSDSS with watershed data
    mcsdss = MCSDSS(None)
    
    # Load data (example with a shapefile)
    mcsdss.load_data(shapefile_path='path/to/watershed.shp')
    
    # Define criteria and weights
    criteria = {
        'water_quality': 0.4,
        'biodiversity': 0.3,
        'land_use': 0.3
    }
    mcsdss.define_criteria(criteria)
    
    # Define scoring functions for each criterion
    scoring_functions = {
        'water_quality': lambda df: df['water_quality_index'],
        'biodiversity': lambda df: df['biodiversity_index'],
        'land_use': lambda df: df['land_use_index']
    }
    mcsdss.score_criteria(scoring_functions)
    
    # Normalize scores
    mcsdss.normalize_scores()
    
    # Aggregate scores
    mcsdss.aggregate_scores()
    
    # Visualize results
    map_result = mcsdss.visualize_results()
    map_result.save('mcsdss_results.html')