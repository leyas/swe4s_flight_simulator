import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import json
from scipy.integrate import solve_ivp
from src.drivers.aeroCalcs import AeroCalcs


class PhysCalcs:
    def __init__(self, rocket_specs_file):
        with open(rocket_specs_file, "r") as file:
            self.rocket_specs = json.load(file)

        self.aero_calcs = AeroCalcs(self.rocket_specs)
        self.motor = self.rocket_specs["motor"]

    def dynamics(self, t, y, burn_time, thrust):
        """Compute the dynamics (velocity and acceleration) of the rocket."""
        x, y_pos, vx, vy, mass = y

        # Prevent negative altitude
        if y_pos <= 0:
            return [0, 0, 0, 0, 0]

        # Calculate velocity magnitude
    
    
        velocity = np.sqrt(vx**2 + vy**2)


        # Determine air density and drag coefficient
        rho = self.aero_calcs.calculate_air_density(y_pos)
        cd = self.aero_calcs.calculate_drag_coefficient(y_pos)
        frontal_area = np.pi * (self.aero_calcs.airframe["diameter"] * 2.54 / 2) ** 2 / 10000  # cm² to m²

        # Calculate drag force components
        drag = 0.5 * cd * rho * frontal_area * velocity**2
        drag_x = -drag * (vx / velocity) if velocity > 0 else 0
        drag_y = -drag * (vy / velocity) - mass * 32 if velocity > 0 else -mass * 32

        # Thrust during burn
        current_thrust = thrust if t <= burn_time else 0
        thrust_x = current_thrust * (vx / velocity) if velocity > 0 else 0
        thrust_y = current_thrust * (vy / velocity) if velocity > 0 else 0

        # Acceleration components
        ax = (thrust_x + drag_x) / mass
        ay = (thrust_y + drag_y) / mass

        # Mass loss during burn
        if t <= burn_time:
            mass_loss_rate = self.motor["mass"] / 1000 / burn_time  # kg/s
            dm_dt = -mass_loss_rate
        else:
            dm_dt = 0

        return [vx, vy, ax, ay, dm_dt]

    def simulate(self):
        """Simulate the trajectory using numerical integration."""
        burn_time = self.motor["burn_time"]
        thrust = self.motor["thrust"]
        initial_mass = self.aero_calcs.calculate_center_of_gravity() + self.motor["mass"] / 1000  # Includes motor mass
        initial_state = [1, 1, 1, 100, initial_mass]  # Initial x, y, vx, vy, mass

        # Ascent and coasting phase
        ascent_result = solve_ivp(
            self.dynamics,
            [0, 100],
            initial_state,
            args=(burn_time, thrust),
            dense_output=True,
            max_step=0.1
        )
        t = ascent_result.t
        y0 = ascent_result.y[0]
        y1 = ascent_result.y[1]  # y-position (assuming y1 is the y-position)
        y2 = ascent_result.y[2]
        y3 = ascent_result.y[3]  # y-velocity (assuming y3 is the y-velocity)

        # Loop over the time steps and check if y1 == 0, if so set y3 to 0 at the corresponding time step
        for i in range(len(y1)):
            if y1[i] <= 0.1:  # When y-position is 0 (i.e., the rocket hits the ground)
                 # Set y-velocity to 0 when the rocket reaches the ground
                y3[i] = 0
                
        return t, y0, y1, y2, y3

    def plot_position_with_gradient(self, x, y, vx, vy):
        """Plot x, y positions with a color gradient based on velocity."""
        # Ensure inputs are numpy arrays
        x = np.asarray(x)
        y = np.asarray(y)
        vx = np.asarray(vx)
        vy = np.asarray(vy)

        # Validate inputs
        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")
        if len(vx) != len(vy):
            raise ValueError("vx and vy must have the same length.")
        if len(x) != len(vx):
            raise ValueError("x, y, vx, and vy must all have the same length.")

        # Calculate velocity magnitude
        
        velocity = np.sqrt(vx**2 + vy**2)
        
    
        # Normalize velocities for coloring
        norm = plt.Normalize(velocity.min(), velocity.max())

        # Prepare the figure and axis
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title("Rocket Trajectory with Velocity Gradient")
        ax.set_xlabel("X Position (m)")
        ax.set_ylabel("Y Position (m)")
        ax.grid()

        # Create a LineCollection for the gradient
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap="viridis", norm=norm)
        lc.set_array(velocity)
        lc.set_linewidth(2)
        ax.add_collection(lc)

        # Set axis limits
        ax.set_xlim(x.min() - 10, x.max() + 10)
        ax.set_ylim(y.min() - 10, y.max() + 10)

        # Add a colorbar
        cbar = plt.colorbar(lc, ax=ax)
        cbar.set_label("Velocity (m/s)")

        plt.show()

    def plot_y_position_with_gradient(self, time, y, velocity):
        """Plot y position over time with a color gradient based on velocity."""
        # Ensure inputs are numpy arrays
        time = np.asarray(time)
        y = np.asarray(y)
        velocity = np.asarray(velocity)

        # Validate inputs
        if len(time) != len(y):
            raise ValueError("time and y must have the same length.")
        if len(velocity) != len(time):
            raise ValueError("velocity and time must have the same length.")

        # Normalize velocities for coloring
        norm = plt.Normalize(velocity.min(), velocity.max())

        # Prepare the figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title("Rocket Y-Position Over Time with Velocity Gradient")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Y Position (m)")
        ax.grid()

        # Create a LineCollection for the gradient
        points = np.array([time, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap="viridis", norm=norm)
        lc.set_array(velocity)
        lc.set_linewidth(2)
        ax.add_collection(lc)

        # Set axis limits
        ax.set_xlim(time.min(), time.max())
        ax.set_ylim(y.min() - 10, y.max() + 10)

        # Add a colorbar
        cbar = plt.colorbar(lc, ax=ax)
        cbar.set_label("Velocity (m/s)")

        plt.show()



if __name__ == "__main__":
    # Create an instance
    material = "blue_tube"
    phys_calcs = PhysCalcs("../config/rocket_specs.json")

    # Simulate the trajectory
    time, x, y, vx, vy = phys_calcs.simulate()

    # Calculate velocity magnitude
   
    velocity = np.sqrt(vx**2 + vy**2)
    

    # Plot y-position over time with velocity gradient
    phys_calcs.plot_y_position_with_gradient(time, y, velocity)

    # Plot position with gradient
    # phys_calcs.plot_position_with_gradient(x, y, vx, vy)
