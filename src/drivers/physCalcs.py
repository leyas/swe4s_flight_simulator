import numpy as np
import matplotlib.pyplot as plt
import json
from scipy.integrate import solve_ivp
from aeroCalcs import AeroCalcs  # Import AeroCalcs


class PhysCalcs:
    def __init__(self, rocket_specs_file, material="fiberglass", motor="K"):
        with open(rocket_specs_file, "r") as file:
            self.rocket_specs = json.load(file)

        self.aero_calcs = AeroCalcs(self.rocket_specs, material=material, motor=motor)
        self.motor = self.rocket_specs["motors"][motor]
        self.parachute = self.rocket_specs["parachute"]

    def dynamics(self, t, y, burn_time, thrust):
        """Compute the dynamics (velocity and acceleration) of the rocket."""
        position, velocity, mass = y

        # Prevent negative altitude
        if position < 0:
            return [0, 0, 0]

        # Determine air density and drag coefficient
        rho = self.aero_calcs.calculate_air_density(position)
        cd = self.aero_calcs.calculate_drag_coefficient(position)
        frontal_area = np.pi * (self.aero_calcs.airframe["diameter"] * 2.54 / 2) ** 2 / 10000  # cm² to m²

        # Calculate drag force
        drag = 0.5 * cd * rho * frontal_area * velocity ** 2 * np.sign(velocity)

        # Thrust during burn, 0 afterward
        current_thrust = thrust if t <= burn_time else 0

        # Calculate acceleration
        acceleration = (current_thrust - drag) / mass - 9.81  # Gravity acts downward

        # Mass loss during burn
        if t <= burn_time:
            mass_loss_rate = self.motor["mass"] / 1000 / burn_time  # kg/s
            dm_dt = -mass_loss_rate
        else:
            dm_dt = 0

        return [velocity, acceleration, dm_dt]

    def apogee_event(self, t, y, *args):
        """Event to stop integration at apogee (velocity = 0)."""
        return y[1]  # Velocity

    apogee_event.terminal = True  # Stop integration at apogee
    apogee_event.direction = -1  # Detect when velocity decreases through zero

    def ground_event(self, t, y, *args):
        """Event to stop integration when rocket hits the ground (position = 0)."""
        return y[0]  # Position

    ground_event.terminal = True  # Stop integration at ground
    ground_event.direction = -1  # Detect when position decreases through zero

    def simulate(self):
        """Simulate the trajectory using numerical integration."""
        burn_time = self.motor["burn_time"]
        thrust = self.motor["thrust"]
        initial_mass = self.aero_calcs.calculate_center_of_gravity() + self.motor["mass"] / 1000  # Includes motor mass
        initial_state = [0, 0, initial_mass]  # Initial position, velocity, mass

        # Ascent and coasting phase
        ascent_result = solve_ivp(
            self.dynamics,
            [0, 100],
            initial_state,
            args=(burn_time, thrust),
            dense_output=True,
            events=self.apogee_event,
            max_step=0.1
        )

        # Get apogee state
        apogee_state = ascent_result.y[:, -1]
        apogee_time = ascent_result.t[-1]
        print(f"Apogee reached at {apogee_state[0]:.2f} meters, time: {apogee_time:.2f} seconds")

        # Descent phase
        descent_result = solve_ivp(
            self.dynamics,
            [apogee_time, apogee_time + 1000],
            apogee_state,
            args=(0, 0),  # No thrust during descent
            dense_output=True,
            events=self.ground_event,
            max_step=0.1
        )

        # Combine results
        time = np.hstack((ascent_result.t, descent_result.t))
        position = np.hstack((ascent_result.y[0], descent_result.y[0]))
        velocity = np.hstack((ascent_result.y[1], descent_result.y[1]))

        return time, position, velocity

    def plot_trajectory(self, time, position, velocity):
        """Plot position and velocity over time."""
        # Plot position
        plt.figure()
        plt.plot(time, position, label="Position (m)")
        plt.title("Rocket Position vs. Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Position (m)")
        plt.legend()
        plt.grid()

        # Plot velocity
        plt.figure()
        plt.plot(time, velocity, label="Velocity (m/s)", color="orange")
        plt.title("Rocket Velocity vs. Time")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (m/s)")
        plt.legend()
        plt.grid()

        plt.show()

if __name__ == "__main__":
    # Create an instance
    phys_calcs = PhysCalcs("rocket_specs.json", material="fiberglass", motor="K")

    # Simulate the trajectory
    time, position, velocity = phys_calcs.simulate()

    # Plot results
    phys_calcs.plot_trajectory(time, position, velocity)
