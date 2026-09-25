import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import minimize


class ContaminantSourceLocator:
    def __init__(self, num_sensors=15):
        np.random.seed(101)
        # True hidden pollution source location
        self.true_source = np.array([45.0, 60.0])

        # Place stationary sensors randomly in a 100x100 area
        self.sensor_coords = np.random.rand(num_sensors, 2) * 100.0

        # Simulate sensor readings based on inverse distance decay + noise
        true_distances = cdist(self.sensor_coords, [self.true_source]).flatten()
        self.sensor_readings = 500.0 / (true_distances + 2.0) + np.random.normal(0, 1.0, num_sensors)

    def dispersion_model(self, source_guess, coords):
        # Expected concentration decay relative to a guessed source position
        d = cdist(coords, [source_guess]).flatten()
        return 500.0 / (d + 2.0)

    def objective_function(self, guess):
        # Mean squared error between simulated readings and model predictions
        predicted = self.dispersion_model(guess, self.sensor_coords)
        return np.sum((self.sensor_readings - predicted) ** 2)

    def locate_source(self):
        # Initial starting guess at the center of the grid (50, 50)
        initial_guess = np.array([50.0, 50.0])

        result = minimize(self.objective_function, initial_guess, method='Nelder-Mead')
        estimated_source = result.x

        print(f"[Spatial AI] True Source Coordinates: {self.true_source}")
        print(f"[Spatial AI] Estimated Source Coordinates: [{estimated_source[0]:.2f}, {estimated_source[1]:.2f}]")
        return estimated_source


if __name__ == "__main__":
    locator = ContaminantSourceLocator(num_sensors=20)
    locator.locate_source()
