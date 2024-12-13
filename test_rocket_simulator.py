# test_rocket_simulation.py
import unittest
from twodrocketsim import Rocket, Velocity, Position, Simulation

class TestRocketSimulation(unittest.TestCase):

    def test_rocket_initialization(self):
        rocket = Rocket(rocket_id="K", angle=87.0, mass=10.0, burn_time=20, total_time=1000, time_step=0.005, total_impulse=2000)
        self.assertEqual(rocket.rocket_id, "K")
        self.assertEqual(rocket.mass, 10.0)
        self.assertEqual(rocket.burn_time, 20)

    def test_velocity_update(self):
        velocity = Velocity(0, 0)
        velocity.update(1, -9.81, 0.005)
        self.assertAlmostEqual(velocity.vx, 0.005)
        self.assertAlmostEqual(velocity.vy, -0.04905)

    def test_position_update(self):
        position = Position()
        position.update(1, -9.81, 0.005)
        self.assertAlmostEqual(position.x, 0.005)
        self.assertAlmostEqual(position.y, -0.04905)

    def test_simulation_run(self):
        rocket = Rocket(rocket_id="K", angle=87.0, mass=10.0, burn_time=20, total_time=1000, time_step=0.005, total_impulse=2000)
        velocity = Velocity(0, 0)
        position = Position()
        simulation = Simulation(rocket, velocity, position)
        simulation.run()
        self.assertGreater(len(simulation.x_vals), 0)
        self.assertGreater(len(simulation.y_vals), 0)

if __name__ == "__main__":
    unittest.main()
