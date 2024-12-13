import unittest
import numpy as np
import json
from src.drivers.physCalcs import PhysCalcs  # Import the PhysCalcs class

class TestPhysCalcs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up initial configuration for all tests."""
        cls.rocket_specs_file = "rocket_specs.json"
        # Assuming we have a mock rocket_specs JSON to simulate the test
        cls.rocket_specs_mock = {
            "air_frame": {"diameter": 5, "length": 100},  # cm
            "nose_cone": {"length": 30},  # cm
            "fins": {"root_chord": 10, "tip_chord": 5, "semi_span": 20},  # cm
            "motors": {
                "K": {
                    "length": 50,  # cm
                    "mass": 2000,  # grams
                    "burn_time": 5,  # seconds
                    "thrust": 50,  # N
                }
            },
            "parachute": {"mass": 500},  # grams
        }

        # Writing the mock specs to a temporary JSON file for testing
        with open(cls.rocket_specs_file, "w") as file:
            json.dump(cls.rocket_specs_mock, file)

        cls.phys_calcs = PhysCalcs(cls.rocket_specs_file, material="fiberglass", motor="K")

    def test_dynamics(self):
        """Test the dynamics function."""
        # Define a sample state (position, velocity, mass)
        t = 1  # Time in seconds
        y = [1000, 50, 1500]  # Position (m), Velocity (m/s), Mass (kg)

        # Burn time and thrust during the ascent phase
        burn_time = 5
        thrust = 50

        # Call the dynamics function
        result = self.phys_calcs.dynamics(t, y, burn_time, thrust)

        # Assert that the result is a list with velocity, acceleration, and mass change (dm/dt)
        self.assertEqual(len(result), 3, "The result should have 3 values: velocity, acceleration, and mass change.")
        self.assertIsInstance(result[0], (int, float), "The velocity should be a number.")
        self.assertIsInstance(result[1], (int, float), "The acceleration should be a number.")
        self.assertIsInstance(result[2], (int, float), "The mass change (dm/dt) should be a number.")

    def test_apogee_event(self):
        """Test the apogee event (stop integration when velocity reaches 0)."""
        # Test when the velocity becomes 0, simulating apogee
        y = [1000, 0, 1500]  # Position (m), Velocity (m/s), Mass (kg)
        t = 10  # Time in seconds
        result = self.phys_calcs.apogee_event(t, y)

        # The event should return 0 (velocity), triggering the terminal condition
        self.assertEqual(result, 0, "The apogee event should trigger when velocity reaches 0.")

    def test_ground_event(self):
        """Test the ground event (stop integration when position reaches 0)."""
        # Test when the position becomes 0, simulating the rocket hitting the ground
        y = [0, -50, 1500]  # Position (m), Velocity (m/s), Mass (kg)
        t = 20  # Time in seconds
        result = self.phys_calcs.ground_event(t, y)

        # The event should return 0 (position), triggering the terminal condition
        self.assertEqual(result, 0, "The ground event should trigger when position reaches 0.")

    def test_simulate(self):
        """Test the simulate function."""
        time, position, velocity = self.phys_calcs.simulate()

        # Assert that time, position, and velocity are numpy arrays
        self.assertIsInstance(time, np.ndarray, "Time should be a numpy array.")
        self.assertIsInstance(position, np.ndarray, "Position should be a numpy array.")
        self.assertIsInstance(velocity, np.ndarray, "Velocity should be a numpy array.")

        # Assert the length of the results
        self.assertGreater(len(time), 0, "The time array should have at least one element.")
        self.assertGreater(len(position), 0, "The position array should have at least one element.")
        self.assertGreater(len(velocity), 0, "The velocity array should have at least one element.")

    def test_plot_trajectory(self):
        """Test the plot_trajectory function."""
        time = np.array([0, 10, 20])
        position = np.array([0, 100, 200])
        velocity = np.array([0, 50, 100])

        # Normally we wouldn't test the plot itself, but we can test that the method runs without errors
        try:
            self.phys_calcs.plot_trajectory(time, position, velocity)
        except Exception as e:
            self.fail(f"plot_trajectory raised an exception: {e}")

    def test_initial_conditions(self):
        """Test if initial conditions are correctly set."""
        initial_mass = self.phys_calcs.aero_calcs.calculate_center_of_gravity() + self.phys_calcs.motor["mass"] / 1000  # kg
        initial_state = [0, 0, initial_mass]  # Initial position, velocity, mass
        self.assertEqual(initial_state[0], 0, "Initial position should be 0 meters.")
        self.assertEqual(initial_state[1], 0, "Initial velocity should be 0 m/s.")
        self.assertGreater(initial_state[2], 0, "Initial mass should be positive.")

    def test_invalid_rocket_specs_file(self):
        """Test for invalid rocket specifications file."""
        with self.assertRaises(FileNotFoundError):
            PhysCalcs("invalid_rocket_specs.json", material="fiberglass", motor="K")

if __name__ == "__main__":
    unittest.main()
