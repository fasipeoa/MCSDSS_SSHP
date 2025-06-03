### Virtual Code Structure for MCSDSS Application

```python
# Import necessary libraries
import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

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
        return gpd.GeoDataFrame(geometry=geometry)

    def set_criteria_weights(self, criteria_weights):
        """Set weights for each criterion."""
        self.criteria_weights = criteria_weights

    def evaluate_criteria(self, criteria_functions):
        """Evaluate criteria using provided functions."""
        for criterion, function in criteria_functions.items():
            self.criteria_scores[criterion] = function(self.watershed_data)

    def aggregate_scores(self):
        """Aggregate scores based on criteria weights."""
        total_score = np.zeros(len(self.watershed_data))
        for criterion, score in self.criteria_scores.items():
            weight = self.criteria_weights.get(criterion, 0)
            total_score += weight * score
        return total_score

    def visualize_results(self, scores):
        """Visualize the results on a map."""
        self.watershed_data['Score'] = scores
        self.watershed_data.plot(column='Score', cmap='viridis', legend=True)
        plt.title('MCSDSS Results')
        plt.show()

    def run(self, criteria_weights, criteria_functions):
        """Run the MCSDSS process."""
        self.set_criteria_weights(criteria_weights)
        self.evaluate_criteria(criteria_functions)
        scores = self.aggregate_scores()
        self.visualize_results(scores)

# Example usage
if __name__ == "__main__":
    # Define watershed data
    watershed = MCSDSS(None)

    # Load data (example shapefile path or lat/lon coordinates)
    watershed.load_data(shapefile_path='path/to/watershed.shp')

    # Define criteria weights
    criteria_weights = {
        'Water Quality': 0.4,
        'Biodiversity': 0.3,
        'Land Use': 0.3
    }

    # Define criteria evaluation functions
    def water_quality(data):
        # Placeholder for actual water quality evaluation logic
        return np.random.rand(len(data))

    def biodiversity(data):
        # Placeholder for actual biodiversity evaluation logic
        return np.random.rand(len(data))

    def land_use(data):
        # Placeholder for actual land use evaluation logic
        return np.random.rand(len(data))

    criteria_functions = {
        'Water Quality': water_quality,
        'Biodiversity': biodiversity,
        'Land Use': land_use
    }

    # Run the MCSDSS application
    watershed.run(criteria_weights, criteria_functions)
```

### Explanation of the Code Structure

1. **Imports**: The necessary libraries for geospatial analysis and data manipulation are imported.

2. **MCSDSS Class**: This class encapsulates the functionality of the MCSDSS application. It includes methods for loading data, setting criteria weights, evaluating criteria, aggregating scores, and visualizing results.

3. **Data Loading**: The `load_data` method allows loading watershed data from a shapefile or creating a GeoDataFrame from latitude and longitude coordinates.

4. **Criteria Evaluation**: The `evaluate_criteria` method takes a dictionary of criteria and their corresponding evaluation functions, which should be defined based on the specific analysis required.

5. **Score Aggregation**: The `aggregate_scores` method combines the scores based on the defined weights.

6. **Visualization**: The `visualize_results` method uses Matplotlib to plot the results on a map.

7. **Run Method**: The `run` method orchestrates the entire process, from setting weights to visualizing results.

### Adaptability
- The application can be adapted to different watersheds by changing the shapefile or latitude/longitude inputs.
- The criteria evaluation functions can be customized based on specific needs and data availability.

### Testing
- The application can be tested across various watersheds by providing different shapefiles or coordinates, ensuring its general applicability.

This virtual code serves as a foundational framework for building a comprehensive MCSDSS application. You can expand upon it by adding more sophisticated criteria evaluation methods, user interfaces, and data sources as needed.