// MCSDSS Application Structure

class MCSDSS:
    def __init__(self):
        self.watershed_data = None
        self.criteria = []
        self.weights = []
        self.results = None

    def load_data(self, source):
        // Load watershed data from shapefile or latitude/longitude
        if is_shapefile(source):
            self.watershed_data = load_shapefile(source)
        else:
            self.watershed_data = load_coordinates(source)

    def define_criteria(self, criteria_list):
        // Define the criteria for decision making
        self.criteria = criteria_list

    def set_weights(self, weights_list):
        // Set the weights for each criterion
        self.weights = weights_list

    def analyze(self):
        // Perform multicriteria analysis
        self.results = perform_mca(self.watershed_data, self.criteria, self.weights)

    def visualize_results(self):
        // Visualize the results on a map
        create_map(self.results)

    def export_results(self, format):
        // Export results to a specified format (e.g., CSV, GeoJSON)
        if format == "CSV":
            export_to_csv(self.results)
        elif format == "GeoJSON":
            export_to_geojson(self.results)

    def run(self, source, criteria_list, weights_list):
        self.load_data(source)
        self.define_criteria(criteria_list)
        self.set_weights(weights_list)
        self.analyze()
        self.visualize_results()
        self.export_results("CSV")


// Helper Functions

def is_shapefile(source):
    // Check if the source is a shapefile
    return source.endswith('.shp')

def load_shapefile(filepath):
    // Load shapefile data
    return read_shapefile(filepath)

def load_coordinates(lat_long):
    // Load data based on latitude and longitude
    return read_coordinates(lat_long)

def perform_mca(data, criteria, weights):
    // Perform multicriteria analysis
    return mca_algorithm(data, criteria, weights)

def create_map(results):
    // Create a map visualization of the results
    map = initialize_map()
    add_results_to_map(map, results)
    display_map(map)

def export_to_csv(results):
    // Export results to CSV file
    with open('results.csv', 'w') as file:
        write_csv(file, results)

def export_to_geojson(results):
    // Export results to GeoJSON file
    with open('results.geojson', 'w') as file:
        write_geojson(file, results)


// Main Execution

if __name__ == "__main__":
    mcsdss = MCSDSS()
    source = get_user_input("Enter shapefile path or latitude/longitude:")
    criteria_list = get_user_input("Enter criteria (comma-separated):").split(',')
    weights_list = list(map(float, get_user_input("Enter weights (comma-separated):").split(',')))
    
    mcsdss.run(source, criteria_list, weights_list)