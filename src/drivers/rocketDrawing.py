import matplotlib.pyplot as plt
import numpy as np

class RocketDrawing:
    def __init__(self, rocket_specs, cg, cp):
        self.rocket_specs = rocket_specs
        self.cg = cg  # Center of Gravity
        self.cp = cp  # Center of Pressure
        self.motor = self.rocket_specs["motors"]["K"]

        # Extract rocket components
        self.airframe = self.rocket_specs["air_frame"]
        self.nose_cone = self.rocket_specs["nose_cone"]
        self.fins = self.rocket_specs["fins"]

        # Create a plot
        self.fig, self.ax = plt.subplots()

    def draw_airframe(self,ax):
        diameter = self.airframe["diameter"]
        length = self.airframe["length"]

        if diameter > 0 and length > 0:
            airframe_x = np.array([0, 0, length, length, 0])
            airframe_y = np.array([-diameter / 2, diameter / 2, diameter / 2, -diameter / 2, -diameter / 2])
            ax.plot(airframe_x, airframe_y, color='blue')
        else:
            print("Airframe dimensions are invalid (zero or negative).")

    def draw_nose_cone(self,ax):
        diameter = self.airframe["diameter"]
        length = self.nose_cone["length"]
        shape = self.nose_cone["shape"]
        airframe_length = self.airframe["length"]

        if length > 0:
            if shape == "conic":
                nose_x = np.array([airframe_length, airframe_length + length, airframe_length])
                nose_y = np.array([-diameter / 2, 0, diameter / 2])
                ax.plot(nose_x, nose_y, color='green')
            elif shape == "elliptic":
                theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
                nose_x = airframe_length + length * np.cos(theta)
                nose_y = (diameter / 2) * np.sin(theta)
                ax.plot(nose_x, nose_y, color='purple')
            elif shape == "tangent_ogive":
                # Parabolic nose cone
                a = (diameter / 2) / (length**2)  # Corrected coefficient
                nose_x = np.linspace(airframe_length, airframe_length + length, 100)
                nose_y = a * (nose_x - airframe_length)**2 - (diameter / 2)
                ax.plot(nose_x, nose_y, color='red')  # Top curve
                ax.plot(nose_x, -nose_y, color='red')  # Bottom curve
                # # Tangent ogive nose cone
                # radius = (length**2 + (diameter / 2)**2) / (2 * (diameter / 2))
                # center_x = airframe_length + length - radius
                # theta = np.linspace(np.arcsin(-diameter / (2 * radius)), np.arcsin(diameter / (2 * radius)), 100)
                # nose_x = center_x + radius * np.cos(theta)
                # nose_y = radius * np.sin(theta)
                # # Draw the top and bottom arcs, ensuring connection to the airframe
                # ax.plot(nose_x, nose_y, color='orange')
                # ax.plot(nose_x, -nose_y, color='orange')
            elif shape == "parabolic":
                # Parabolic nose cone
                a = (diameter / 2) / (length**2)  # Corrected coefficient
                nose_x = np.linspace(airframe_length, airframe_length + length, 100)
                nose_y = a * (nose_x - airframe_length)**2 - (diameter / 2)
                ax.plot(nose_x, nose_y, color='red')  # Top curve
                ax.plot(nose_x, -nose_y, color='red')  # Bottom curve
            else:
                print(f"Unknown nose cone shape: {shape}. Skipping nose cone.")
        else:
            print("Nose cone length is invalid (zero or negative).")

    def draw_fins(self,ax):
        """Plot the fins symmetrically on both sides of the rocket."""
        root_chord = self.fins["root_chord"]  # Root chord length in inches
        tip_chord = self.fins["tip_chord"]  # Tip chord length in inches
        semi_span = self.fins["semi_span"]  # Semi-span in inches
        sweep_angle_deg = self.fins["sweep_angle"]  # Sweep angle in degrees
        diameter = self.airframe["diameter"]  # Airframe diameter in inches

        if root_chord > 0 and semi_span > 0:
            # Convert sweep angle to radians
            sweep_angle_rad = np.radians(sweep_angle_deg)

            # Reverse the orientation of the fin tip's x-coordinate
            #fin_tip_x = root_chord - (semi_span * np.tan(sweep_angle_rad)) + tip_chord
            fin_tip_x = root_chord * np.cos(sweep_angle_rad) + (semi_span * np.sin(sweep_angle_rad))

            # for sign in [-1, 1]:  # Top (+1) and bottom (-1) fins
            #     # Define the fin polygon points
            #     fin_base_x = np.array([0, root_chord, fin_tip_x, 0])
            #     fin_base_y = np.array([
            #         sign * diameter / 2,  # Start at the airframe edge
            #         sign * diameter / 2,  # Root chord position
            #         sign * (diameter / 2 + semi_span),  # Tip of the fin
            #         sign * diameter / 2  # Return to airframe edge
            #     ])
            # for sign in [-1, 1]:  # Top (+1) and bottom (-1) fins
            #     # Define the fin polygon points
            #     fin_base_x = np.array([0, fin_tip_x, root_chord, 0])
            #     fin_base_y = np.array([
            #         sign * diameter / 2,  # Start at the airframe edge
            #         sign * diameter / 2,  # Root chord position
            #         sign * (diameter / 2 + semi_span),  # Tip of the fin
            #         sign * diameter / 2  # Return to airframe edge
            #     ])
            for sign in [-1, 1]:  # Top (+1) and bottom (-1) fins
                # Define the fin polygon points
                fin_base_x = np.array([0, 0, tip_chord, root_chord])
                fin_base_y = np.array([
                    sign * (diameter / 2),  # Start at the airframe edge
                    sign * semi_span,  # Root chord position
                    sign * semi_span,  # Tip of the fin
                    sign * (diameter / 2) # Return to airframe edge
                ])

                # Plot the fin
                ax.plot(fin_base_x, fin_base_y, color='red')
        else:
            print("Fin dimensions are invalid (zero or negative).")

    def draw_motor(self, ax):
        """Plot the motor at the aft end of the rocket."""
        motor_diameter = self.motor["diameter"] / 25.4  # Convert mm to inches
        motor_length = self.motor["length"] / 25.4  # Convert mm to inches
        airframe_diameter = self.airframe["diameter"]

        motor_x = np.array([0, motor_length, motor_length, 0, 0])
        motor_y = np.array([-motor_diameter / 2, -motor_diameter / 2, motor_diameter / 2, motor_diameter / 2, -motor_diameter / 2])

        # Motor rectangle dimensions
        motor_x = np.array([0, motor_length, motor_length, 0, 0])
        motor_y = np.array([-motor_diameter / 2, -motor_diameter / 2, motor_diameter / 2, motor_diameter / 2, -motor_diameter / 2])

        ax.plot(motor_x, motor_y, color='orange', label='Motor')

    def draw_cg_cp(self, ax):
        """Plot CG and CP as points on the rocket."""
        diameter = self.airframe["diameter"]

        # Plot CG as a red dot
        ax.scatter([self.cg], [0], color='red', s=50, label='CG')

        # Plot CP as a blue dot
        ax.scatter([self.cp], [0], color='blue', s=50, label='CP')

        # Add labels
        ax.text(self.cg, diameter / 2 + 0.5, "CG", color='red', fontsize=10, ha='center')
        ax.text(self.cp, -diameter / 2 - 0.5, "CP", color='blue', fontsize=10, ha='center')

        # ax.scatter(0, self.cg, color="red", label="CG", zorder=5)
        # ax.scatter(0, self.cp, color="orange", label="CP", zorder=5)

    def plot_rocket(self, ax):
        """
        Plot the rocket design on the provided Matplotlib axis.
        """
        # Clear the axis for fresh plotting
        ax.clear()

        # Example: Drawing a simple outline of the rocket
        self.draw_airframe(ax)
        self.draw_nose_cone(ax)
        self.draw_fins(ax)
        self.draw_motor(ax)
        self.draw_cg_cp(ax)

        # Formatting the plot
        ax.set_aspect('equal')
        ax.set_title("Rocket Outline with CG and CP")
        ax.set_xlabel("Length (inches)")
        ax.set_ylabel("Width (inches)")
        ax.grid(True)