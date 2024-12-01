import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# Constants
g = 9.81  # acceleration due to gravity (m/s^2)
rho = 1.225  # air density (kg/m³) at sea level
cd_fuselage = 0.5
cd_nose_cone = 0.3
cd_fin = 0.3
area_fuselage = 0.1  # cross-sectional area of fuselage (m²)
fin_area = 0.02  # area of one fin (m²)
num_fins = 4  # number of fins on the rocket
rocket_id = "K"  # Rocket identifier (adjust this based on your specs)

# Function to load rocket specs from CSV
def load_rocket_specs(file_path):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return {row["Rocket"]: float(row["Total_Impulse"]) for row in reader}
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return {}

class Position:
    def __init__(self):
        self.x, self.y = 0, 0

    def update(self, vx, vy, time_step):
        self.x += vx * time_step
        self.y += vy * time_step

class Velocity:
    def __init__(self, initial_vx=0, initial_vy=0):
        self.vx, self.vy = initial_vx, initial_vy

    def update(self, ax, ay, time_step):
        self.vx += ax * time_step
        self.vy += ay * time_step

    def apply_drag(self, speed, vx, vy, time_step, rocket):
        cd_effective = 0.2 + 0.1 * np.tanh(speed / 50)
        max_cd_effective = 1.5
        cd_effective = np.min([cd_effective, max_cd_effective])

        total_drag = cd_effective * rho * (area_fuselage + fin_area * num_fins) * speed**2 / 2

        drag_x = np.arccos(vy/vx) * total_drag * vx / speed
        drag_y = np.arcsin(vy/vx) * total_drag * vy / speed 

        self.vx -= drag_x * time_step
        self.vy -= drag_y * time_step

        # Apply parachute drag only if deployed
        if rocket.parachute_deployed:
            # Reduce parachute drag based on speed
            parachute_drag = 0.5 * rocket.parachute_drag_coeff * rho * rocket.parachute_area * self.vy**2

            # Reduce drag as vertical velocity slows down
            if self.vy < -10:  # Once vertical velocity is small enough, reduce parachute drag
                parachute_drag *= 0.5  # Reduce by 50%

            self.vy -= parachute_drag * time_step
            self.vy = max(self.vy, -0.5)  # Prevent hovering

class Rocket:
    def __init__(self, rocket_id, angle, mass, burn_time, total_time, time_step, total_impulse):
        self.thrust = total_impulse / burn_time
        self.angle_rad = np.radians(angle)
        self.mass = mass
        self.burn_time = burn_time
        self.time_step = time_step
        self.total_time = total_time
        self.parachute_deployed = False
        self.parachute_drag_coeff = 4.0  # Moderate parachute drag
        self.rocket_id = rocket_id
        self.parachute_area = area_fuselage * 4  # Reasonable parachute area

    def get_acceleration(self, thrust_active, t):
        thrust_factor = np.exp(-0.01 * t) if t <= self.burn_time else 0.2
        thrust = self.thrust * thrust_factor

        if thrust_active:
            ax = thrust * np.cos(self.angle_rad) / self.mass
            ay = thrust * np.sin(self.angle_rad) / self.mass
        else:
            ax, ay = 0, -g
        return ax, ay

class Simulation:
    def __init__(self, rocket, velocity, position):
        self.rocket = rocket
        self.velocity = velocity
        self.position = position
        self.time = np.arange(0, rocket.total_time, rocket.time_step)
        self.x_vals, self.y_vals = [], []

    def run(self):
        max_height = 0
        burn_end_time = self.rocket.burn_time
        parachute_time = 0  # Time during parachute descent phase
        max_parachute_time = 200.0  # Max time for parachute descent to avoid forever simulation

        for t in self.time:
            thrust_active = t <= self.rocket.burn_time
            ax, ay = self.rocket.get_acceleration(thrust_active, t)

            self.velocity.update(ax, ay, self.rocket.time_step)

            speed = np.sqrt(self.velocity.vx**2 + self.velocity.vy**2)
            self.velocity.apply_drag(speed, self.velocity.vx, self.velocity.vy, self.rocket.time_step, self.rocket)

            self.position.update(self.velocity.vx, self.velocity.vy, self.rocket.time_step)

            if self.position.y > max_height:
                max_height = self.position.y

            self.x_vals.append(self.position.x)
            self.y_vals.append(self.position.y)

            # Parachute deployment logic
            if not self.rocket.parachute_deployed and self.velocity.vy < -3:  # Lower descent threshold
                self.rocket.parachute_deployed = True

            # Increase time step during parachute descent phase
            if self.rocket.parachute_deployed:
                parachute_time += self.rocket.time_step
                if parachute_time > max_parachute_time:
                    break  # Stop simulation after max parachute descent time

                # Increase time step during parachute phase to speed up simulation
                parachute_time_step = 0.02  # 0.02 seconds instead of 0.01 for faster descent
                self.velocity.update(ax, ay, parachute_time_step)
                self.position.update(self.velocity.vx, self.velocity.vy, parachute_time_step)

            if self.position.y < 0:
                break

        # Plot the results
        plt.figure(figsize=(10, 6))
        plt.plot(self.x_vals, self.y_vals, label='Flight Path')

        plt.axvline(x=self.x_vals[int(burn_end_time / self.rocket.time_step)], color='r', linestyle='--', label='Burn End')
        plt.axhline(y=max_height, color='g', linestyle='--', label=f'Max Height = {max_height:.2f} m')

        plt.xlabel('Distance (m)')
        plt.ylabel('Height (m)')
        plt.title(f'Rocket {self.rocket.rocket_id} Flight Path with Thrust, Drag, and Parachute')

        padding = max(self.y_vals) / 10
        plt.xlim(0, max(self.x_vals) + padding)
        plt.ylim(0, max(self.y_vals) + padding)

        plt.grid(True)
        plt.axhline(0, color='black', lw=0.5, ls='--')  # Ground line
        plt.legend()

        plt.show()

def main():
    csv_file = 'rocket_specs.csv'
    if not os.path.exists(csv_file):
        print(f"Error: The file '{csv_file}' does not exist.")
        return

    rocket_specs = load_rocket_specs(csv_file)

    if rocket_id not in rocket_specs:
        print(f"Rocket specs for '{rocket_id}' not found!")
        return

    total_impulse = rocket_specs[rocket_id]

    # User-defined inputs
    angle, mass, burn_time, time_step, total_time = 87.0, 10.0, 20, 0.005, 1000.0  # Adjusted time_step

    rocket = Rocket(rocket_id, angle, mass, burn_time, total_time, time_step, total_impulse)
    velocity = Velocity()
    position = Position()

    simulation = Simulation(rocket, velocity, position)
    simulation.run()

if __name__ == '__main__':
    main()
