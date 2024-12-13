import unittest
from src.drivers.aeroCalcs import AeroCalcs

class TestAeroCalcs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the initial configuration for all tests"""
        # A mock `rocket_specs` dictionary with basic test data
        cls.rocket_specs = {
            "air_frame": {"diameter": 5, "length": 100},  # cm
            "nose_cone": {"length": 30},  # cm
            "fins": {"root_chord": 10, "tip_chord": 5, "semi_span": 20},  # cm
            "motors": {"K": {"length": 50, "mass": 2000}},  # cm, grams
            "parachute": {"mass": 500},  # grams
            "materials": {
                "fg_density": 1.5,  # g/cm³ (fiberglass density)
                "bt_density": 1.2,  # g/cm³ (cardboard tube density)
                "thickness": 3,  # mm
            }
        }
        cls.aero = AeroCalcs(cls.rocket_specs)

    def test_calculate_air_density_troposphere(self):
        """Test air density in the troposphere (altitude < 11000 m)"""
        altitude = 5000  # meters
        expected_density = self.aero.calculate_air_density(altitude)
        self.assertAlmostEqual(expected_density, 0.736, places=3, msg="Density at 5000m should be approximately 0.736 g/cm³")

    def test_calculate_air_density_stratosphere(self):
        """Test air density in the stratosphere (altitude > 11000 m)"""
        altitude = 12000  # meters
        expected_density = self.aero.calculate_air_density(altitude)
        self.assertAlmostEqual(expected_density, 0.236, places=3, msg="Density at 12000m should be approximately 0.236 g/cm³")

    def test_calculate_center_of_gravity(self):
        """Test calculation of the center of gravity (CG)"""
        expected_cg = self.aero.calculate_center_of_gravity()
        self.assertAlmostEqual(expected_cg, 54.02, places=2, msg="CG should be approximately 54.02 inches")

    def test_calculate_center_of_pressure(self):
        """Test calculation of the center of pressure (CP)"""
        expected_cp = self.aero.calculate_center_of_pressure()
        self.assertAlmostEqual(expected_cp, 47.08, places=2, msg="CP should be approximately 47.08 inches")

    def test_calculate_drag_coefficient(self):
        """Test calculation of the drag coefficient (Cd)"""
        altitude = 1000  # meters
        expected_cd = self.aero.calculate_drag_coefficient(altitude)
        self.assertAlmostEqual(expected_cd, 0.351, places=3, msg="Drag coefficient should be approximately 0.351")

    def test_calculate_drag_force(self):
        """Test calculation of the drag force at a given velocity"""
        altitude = 1000  # meters
        velocity = 150  # m/s
        expected_drag_force = self.aero.calculate_drag_force(altitude, velocity)
        self.assertAlmostEqual(expected_drag_force, 24.50, places=2, msg="Drag force should be approximately 24.50 N")

    def test_calculate_center_of_gravity_with_alternate_material(self):
        """Test calculation of CG with a different material (cardboard)"""
        # Change material to "cardboard"
        self.aero.material = "cardboard"
        self.aero.density = self.aero.materials["bt_density"]
        expected_cg = self.aero.calculate_center_of_gravity()
        self.assertAlmostEqual(expected_cg, 54.02, places=2, msg="CG should be approximately 54.02 inches for cardboard")

    def test_invalid_altitude(self):
        """Test for invalid altitude (e.g., negative)"""
        with self.assertRaises(ValueError):
            self.aero.calculate_air_density(-500)

    def test_invalid_motor_choice(self):
        """Test if invalid motor selection raises an error"""
        with self.assertRaises(KeyError):
            AeroCalcs(self.rocket_specs, motor="invalid_motor")

    def test_missing_material_property(self):
        """Test for missing material property (e.g., if the material doesn't exist)"""
        self.aero.material = "plastic"  # Assuming 'plastic' is not in the materials dict
        with self.assertRaises(KeyError):
            self.aero.density  # This should raise a KeyError because 'plastic' is not defined

if __name__ == "__main__":
    unittest.main()
