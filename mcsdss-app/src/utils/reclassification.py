# Import necessary libraries
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point
import folium  # For mapping
from sklearn.preprocessing import MinMaxScaler

# Define the MCSDSS class
class MCSDSS:
    def __init__(self, watershed_data):
        self.watershed_data = watershed_data  # Load watershed data (shapefile or coordinates)
        self.criteria_weights = {}
        self.criteria_data = {}
    
    def load_data(self, filepath=None, lat_lon=None):
        """Load watershed data from a shapefile or latitude/longitude."""
        if filepath:
            self.watershed_data = gpd.read_file(filepath)
        elif lat_lon:
            self.watershed_data = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in lat_lon])
        else:
            raise ValueError("Provide either a filepath or latitude/longitude data.")
    
    def set_criteria_weights(self, criteria_weights):
        """Set weights for each criterion."""
        self.criteria_weights = criteria_weights
    
    def add_criteria_data(self, criterion_name, data):
        """Add data for a specific criterion."""
        self.criteria_data[criterion_name] = data
    
    def normalize_criteria(self):
        """Normalize criteria data to a common scale."""
        scaler = MinMaxScaler()
        for criterion, data in self.criteria_data.items():
            self.criteria_data[criterion] = scaler.fit_transform(data.values.reshape(-1, 1))
    
    def calculate_scores(self):
        """Calculate scores based on weighted criteria."""
        scores = np.zeros(len(self.watershed_data))
        for criterion, weight in self.criteria_weights.items():
            scores += self.criteria_data[criterion].flatten() * weight
        return scores
    
    def visualize_results(self, scores):
        """Visualize the results on a map."""
        self.watershed_data['Scores'] = scores
        m = folium.Map(location=[self.watershed_data.geometry.y.mean(), self.watershed_data.geometry.x.mean()], zoom_start=10)
        
        for _, row in self.watershed_data.iterrows():
            folium.CircleMarker(location=(row.geometry.y, row.geometry.x),
                                radius=5,
                                color=self.get_color(row['Scores']),
                                fill=True,
                                fill_opacity=0.6).add_to(m)
        
        return m
    
    def get_color(self, score):
        """Get color based on score."""
        if score < 0.3:
            return 'blue'
        elif score < 0.6:
            return 'yellow'
        else:
            return 'green'

# Example usage
if __name__ == "__main__":
    # Initialize MCSDSS
    mcsdss = MCSDSS(None)
    
    # Load data (example with a shapefile)
    mcsdss.load_data(filepath='path/to/watershed.shp')
    
    # Set criteria weights (example)
    mcsdss.set_criteria_weights({'Water Quality': 0.4, 'Land Use': 0.3, 'Biodiversity': 0.3})
    
    # Add criteria data (example)
    mcsdss.add_criteria_data('Water Quality', pd.Series(np.random.rand(len(mcsdss.watershed_data))))
    mcsdss.add_criteria_data('Land Use', pd.Series(np.random.rand(len(mcsdss.watershed_data))))
    mcsdss.add_criteria_data('Biodiversity', pd.Series(np.random.rand(len(mcsdss.watershed_data))))
    
    # Normalize criteria
    mcsdss.normalize_criteria()
    
    # Calculate scores
    scores = mcsdss.calculate_scores()
    
    # Visualize results
    map_result = mcsdss.visualize_results(scores)
    map_result.save('mcsdss_results.html')