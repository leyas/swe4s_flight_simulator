import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81  # acceleration due to gravity (m/s^2)

# Function to simulate projectile motion with thrust and initial velocity
def simulate_rocket(thrust, angle, mass, burn_time, time_step, total_time):
    angle_rad = np.radians(90 - angle)  # Convert angle to radians
    initial_v = 0  # Initial velocity in m/s

    # Calculate thrust acceleration
    ax = thrust * np.cos(angle_rad) / mass  # Acceleration in x-direction
    ay = thrust * np.sin(angle_rad) / mass  # Acceleration in y-direction

    # Time array
    t = np.arange(0, total_time, time_step)
    x = np.zeros_like(t)
    y = np.zeros_like(t)
    
    # Initial velocities
    vx, vy = initial_v, 0

    for i in range(1, len(t)):
        if t[i] <= burn_time:  # While thrust is applied
            vx += ax * time_step
            vy += (ay - g) * time_step  # Thrust up and gravity down
        else:  # After thrust is gone, only gravity affects motion
            vy -= g * time_step  # Gravity only
        
        # Update positions
        x[i] = x[i-1] + vx * time_step
        y[i] = y[i-1] + vy * time_step

        # Stop if the projectile hits the ground
        if y[i] < 0:
            x = x[:i+1]
            y = y[:i+1]
            break

    return x, y, vx, vy, t

# Inputs, user define them once code is better
thrust = 300.0  # N
angle = 3.0  # deg off of 90
mass = 7.0  # total mass (kg)
burn_time = 5.0  # burn duration (sec)
time_step = 0.01  # time step (sec)
total_time = 80.0  # total flight window (sec)

# Simulate rocket flight
x, y, vx, vy, t = simulate_rocket(thrust, angle, mass, burn_time, time_step, total_time)

# Find max height
max_height = max(y)
max_height_time = t[np.argmax(y)]  # Time at which max height occurs
end_of_burn_x = x[int(burn_time / time_step)]  # X position at end of burn

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Flight Path')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')

# Set limits to encapsulate the entire path with some padding for visualization
padding = max_height / 10  # Padding around the trajectory
plt.xlim(0, max(x) + padding)
plt.ylim(0, max(y) + padding)

# Add lines to indicate end of burn and max height
plt.axvline(x=end_of_burn_x, color='r', linestyle='--', label='End of Thrust')
plt.axhline(y=max_height, color='g', linestyle='--', label='Max Height')

# Add annotations for end of burn and max height
plt.annotate('',xy=(end_of_burn_x, 0), xytext=(end_of_burn_x, max_height * 0.5))
plt.annotate(f'Max Height: {max_height:.2f} m', xy=(0, max_height), xytext=(10, max_height + 10))

plt.grid()
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.legend()
plt.show()
