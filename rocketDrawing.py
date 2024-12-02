import json
import matplotlib.pyplot as plt
import math
import numpy as np

class RocketDrawing:
    def __init__(self, json_file):
        try:
            with open(json_file, 'r') as file:
                content = file.read().strip()
                if not content:
                    raise ValueError("The JSON file is empty.")
                self.rocket_specs = json.loads(content)
        except FileNotFoundError:
            print(f"File not found: {json_file}")
            return
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return
        except ValueError as e:
            print(e)
            return
        
        # Extract components from JSON
        self.air_frame = self.rocket_specs.get("air_frame", {})
        self.fins = self.rocket_specs.get("fins", {})
        self.nose_cone = self.rocket_specs.get("nose_cone", {})
        
        # Create a plot
        self.fig, self.ax = plt.subplots()

    def draw_airframe(self):
        diameter = self.air_frame.get("diameter", 0)  # inches
        length = self.air_frame.get("length", 0)  # inches

        if diameter > 0 and length > 0:
            airframe_x = [0, 0, length, length, 0]
            airframe_y = [-diameter / 2, diameter / 2, diameter / 2, -diameter / 2, -diameter / 2]
            self.ax.plot(airframe_x, airframe_y, color='blue')
        else:
            print("Airframe dimensions are invalid (zero or negative).")

    def draw_nose_cone(self):
        diameter = self.air_frame.get("diameter", 0)  # inches
        length = self.nose_cone.get("length", 0)  # inches
        shape = self.nose_cone.get("shape", "unknown")
        airframe_length = self.air_frame.get("length", 0)

        if length > 0:
            if shape == "conic":
                # Conic nose cone
                nose_x = [airframe_length, airframe_length + length, airframe_length]
                nose_y = [-diameter / 2, 0, diameter / 2]
                self.ax.plot(nose_x, nose_y, color='green')
            elif shape == "elliptical":
                # Elliptical nose cone
                theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
                nose_x = airframe_length + (length * np.cos(theta))
                nose_y = (diameter / 2) * np.sin(theta)
                self.ax.plot(nose_x, nose_y, color='purple')
            elif shape == "tangent ogive":
                # Parabolic nose cone
                a = (diameter / 2) / (length**2)  # Corrected coefficient
                nose_x = np.linspace(airframe_length, airframe_length + length, 100)
                nose_y = a * (nose_x - airframe_length)**2 - (diameter / 2)
                self.ax.plot(nose_x, nose_y, color='red')  # Top curve
                self.ax.plot(nose_x, -nose_y, color='red')  # Bottom curve
            else:
                print(f"Unknown nose cone shape: {shape}. Skipping nose cone.")
        else:
            print("Nose cone length is invalid (zero or negative).")

    def draw_fins(self):
        root_chord = self.fins.get("root_chord", 0)  # inches
        tip_chord = self.fins.get("tip_chord", 0)  # inches
        semi_span = self.fins.get("semi_span", 0)  # inches
        sweep_angle_deg = self.fins.get("sweep_angle", 0)  # degrees
        diameter = self.air_frame.get("diameter", 0)  # inches

        if root_chord > 0 and semi_span > 0:
            sweep_angle_rad = math.radians(sweep_angle_deg)
            fin_tip_x = root_chord - tip_chord + semi_span * math.tan(sweep_angle_rad)
            
            for sign in [-1, 1]:  # Top and bottom fins
                fin_base_x = [0, root_chord, fin_tip_x, 0]
                fin_base_y = [sign * diameter / 2,
                              sign * diameter / 2,
                              sign * (diameter / 2 + semi_span),
                              sign * diameter / 2]
                self.ax.plot(fin_base_x, fin_base_y, color='red')
        else:
            print("Fin dimensions are invalid (zero or negative).")

    def plot_rocket(self):
        self.draw_airframe()
        self.draw_nose_cone()
        self.draw_fins()
        
        # Formatting the plot
        self.ax.set_aspect('equal')
        self.ax.set_title("Rocket Outline")
        self.ax.set_xlabel("Length (inches)")
        self.ax.set_ylabel("Width (inches)")
        plt.grid(True)
        plt.show()

# Example Usage
rocket = RocketDrawing("rocket_specs.json")
rocket.plot_rocket()
