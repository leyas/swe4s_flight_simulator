import numpy as np

class AeroCalcs:
    def __init__(self, rocket_specs, parachute_size, material, motor_name): # change later
        self.rocket_specs = rocket_specs
        self.material = material.lower()
        self.motor_name = motor_name

        print(self.rocket_specs["materials"]["blue_tube"]["density"])

        # Load airframe, nose cone, fins, materials, and motor details
        self.airframe = self.rocket_specs["air_frame"]
        self.nose_cone = self.rocket_specs["nose_cone"]
        self.fins = self.rocket_specs["fins"]
        self.motor = self.rocket_specs["motors"][self.motor_name]
        self.parachute = self.rocket_specs["parachute"][parachute_size]
        self.materials = self.rocket_specs["materials"][self.material]

        # Material properties
        self.density = self.materials["density"] 
        self.thickness = self.materials["thickness"] / 10  # Convert mm to cm for calculations

    def calculate_air_density(self, altitude):
        """Calculate air density at a given altitude in g/cm³."""
        if altitude <= 11000:  # Troposphere
            temp = 288.15 - 0.0065 * altitude  # Temperature in Kelvin
            pressure = 101325 * (temp / 288.15) ** 5.2561  # Pressure in Pascals
        else:  # Above troposphere, simplified model
            temp = 216.65  # Temperature constant in Kelvin
            pressure = 22632 * np.exp(-0.0001577 * (altitude - 11000))  # Pressure in Pascals

        density_kg_m3 = pressure / (287.05 * temp)  # Air density in kg/m³
        density_g_cm3 = density_kg_m3 / 1000  # Convert to g/cm³
        return density_g_cm3

    def calculate_center_of_gravity(self):
        """Calculate the center of gravity (CG) in inches."""
        airframe_diameter = self.airframe["diameter"] * 2.54  # Inches to cm
        airframe_length = self.airframe["length"] * 2.54  # Inches to cm
        nose_cone_length = self.nose_cone["length"] * 2.54  # Inches to cm
        motor_length = self.motor["length"] / 10  # mm to cm
        motor_mass = self.motor["mass"]  # Already in grams

        # Calculate masses
        airframe_volume = np.pi * ((airframe_diameter / 2) ** 2 - ((airframe_diameter / 2) - self.thickness) ** 2) * airframe_length
        airframe_mass = airframe_volume * self.density
        nose_cone_volume = (1 / 3) * np.pi * (airframe_diameter / 2) ** 2 * nose_cone_length
        nose_cone_mass = nose_cone_volume * self.density * (self.thickness / (airframe_diameter / 2))
        fin_area = self.fins["root_chord"] * self.fins["semi_span"]
        fin_mass = 3 * fin_area * self.thickness * self.density
        parachute_mass = self.parachute["mass"]

        # Center positions in cm
        cg_airframe = airframe_length / 2
        cg_nose_cone = airframe_length + nose_cone_length / 3
        cg_fins = self.fins["root_chord"] / 2 * 2.54
        cg_motor = motor_length / 2
        cg_parachute = airframe_length + nose_cone_length

        total_mass = airframe_mass + nose_cone_mass + fin_mass + motor_mass + parachute_mass
        cg_cm = (
            (airframe_mass * cg_airframe) +
            (nose_cone_mass * cg_nose_cone) +
            (fin_mass * cg_fins) +
            (motor_mass * cg_motor) +
            (parachute_mass * cg_parachute)
        ) / total_mass

        return cg_cm / 2.54  # Convert CG to inches

    def calculate_center_of_pressure(self):
        """Calculate the center of pressure (CP) in inches."""

        # Dimensions in inches
        nose_length = self.nose_cone["length"]
        body_length = self.airframe["length"]
        root_chord = self.fins["root_chord"]
        tip_chord = self.fins["tip_chord"]
        semi_span = self.fins["semi_span"]

        # Fin area
        fin_area = (root_chord + tip_chord) / 2 * semi_span

        # CP components
        cp_nose = body_length + (nose_length * 0.5)
        cp_body = body_length * 0.5
        cp_fins = ((root_chord - tip_chord) / 2) * fin_area

        # Total CP
        cp_total = (cp_nose + cp_body + cp_fins) / (1 + fin_area)
        

        return cp_total

    def calculate_drag_coefficient(self, altitude):
        """Calculate the drag coefficient (Cd) using Barrowman's model."""
        airframe_diameter = self.airframe["diameter"]
        nose_cone_cd = 0.5 * (self.nose_cone["length"] / airframe_diameter)
        fin_cd = (
            2 * self.fins["semi_span"] ** 2 / (airframe_diameter * self.fins["root_chord"]) *
            (1 + np.sqrt(1 + (self.fins["semi_span"] / self.fins["root_chord"]) ** 2))
        )
        base_cd = 0.029 * (airframe_diameter / self.motor["diameter"])
        total_cd = nose_cone_cd + fin_cd + base_cd
        return total_cd

    def calculate_drag_force(self, altitude, velocity):
        """Calculate drag force at a given altitude and velocity."""
        cd = self.calculate_drag_coefficient(altitude)
        air_density = self.calculate_air_density(altitude)
        frontal_area = np.pi * (self.airframe["diameter"] * 2.54 / 2) ** 2  # cm²
        drag_force = 0.5 * cd * air_density * frontal_area * (velocity * 100) ** 2  # Velocity in cm/s
        return drag_force / 1000  # Convert drag force to N
