# Rocket Flight Simulation Project

## Overview

This project simulates the flight trajectory of a rocket using both **aerodynamic** and **physical** calculations based on user-defined parameters. The goal is to compute the rocket's 1-dimensional flight path (position and velocity) from launch to landing. The simulation accounts for various factors such as airframe dimensions, motor thrust, drag, gravity, and more.

The project includes two primary calculation modules:
- **AeroCalcs**: Performs aerodynamic calculations (e.g., air density, drag coefficient, center of gravity).
- **PhysCalcs**: Handles the physical simulation of the rocket's flight trajectory using numerical integration (e.g., velocity, position, and mass changes).

## Features

- **Input Rocket Parameters**: Define rocket specifications in GUI.
- **Aerodynamic Calculations**: Calculate drag, center of gravity (CG), and other aerodynamic properties.
- **Flight Simulation**: Simulate the rocket's ascent and descent using numerical integration.
- **Trajectory Plotting**: WIll provide a visual showing the rocket's flight path with position and velocity over time.
- **Customizable Material and Motor**: Choose different mass, geometry, and motors for the rocket to see their effects on performance.

## Installation

1. Clone the repository: To clone the repository, run the following command:
   ```bash
   git clone https://github.com/your-username/rocket-flight-simulation.git
2. Install the required Python dependencies: Navigate to the project directory and install the necessary dependencies by running:

'''bash
pip install -r requirements.txt

Ensure you have the necessary files: The project requires a rocket_specs.json file that contains the specifications of the rocket. You can modify this file to define your custom rocket parameters. A sample rocket_specs.json file is included in the repository.

Usage
Define your rocket's specifications in the rocket_specs.json file.
You can adjust the material and motor selection based on the available options in the file.
Run the phys_calcs.py script to simulate the rocket's flight trajectory.
The script will output the rocket's position and velocity at each time step and will also generate a plot of the rocket's trajectory.
Features
Input Rocket Parameters: Define rocket specifications in a JSON file.
Aerodynamic Calculations: Calculate drag, center of gravity (CG), and other aerodynamic properties.
Flight Simulation: Simulate the rocket's ascent and descent using numerical integration.
Trajectory Plotting: Visualize the rocket's flight path with position and velocity over time.
Customizable Material and Motor: Choose different materials and motors for the rocket to see their effects on performance.
Project Structure
rocket_specs.json: The file containing the rocket's specifications.
aeroCalcs.py: A Python file that performs aerodynamic calculations.
physCalcs.py: A Python file that handles the physical simulation of the rocket’s flight.
requirements.txt: A list of dependencies required to run the project.
README.md: This file containing project documentation.
Requirements
Python 3.x
NumPy
Matplotlib
SciPy

