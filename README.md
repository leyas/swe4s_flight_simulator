# Rocket Flight Simulation Project

## Overview

This project simulates the flight trajectory of a rocket using both **aerodynamic** and **physical** calculations based on user-defined parameters. The goal is to compute and visualize the rocket's flight path (position and velocity) from launch to landing. The simulation accounts for various factors such as airframe dimensions, motor thrust, drag, gravity, and more.

The project interacts with the user through our GUI:
- **rocketGUI**: prompts user to input rocket characteristics such as its geometry, motor class, material, and parachute diameter. The flight simulation visual will be returned to the user in this same window after the rocket parameters are used to calculate its flight path.

The GUI interacts with two primary calculation modules:
- **AeroCalcs**: Performs aerodynamic calculations (e.g., air density, drag coefficient, center of gravity).
- **PhysCalcs**: Handles the physical simulation of the rocket's flight trajectory using numerical integration (e.g., velocity, position, and mass changes).

## Features

- **Input Rocket Parameters**: Define rocket specifications in GUI.
- **Aerodynamic Calculations**: Calculate drag, center of gravity (CG), center of aerodynamic pressure (CP) and other aerodynamic properties.
- **Flight Simulation**: Simulate the rocket's ascent and descent through equations of motion.
- **Trajectory Plotting**: Provides a visual showing the rocket's flight path with position and velocity over time.
- **Info Page**: Section in GUI with more information on rocket parameter definitions for beginners.

## Installation

1. Clone the repository: To clone the repository, run the following command:
   ```bash
   git clone https://github.com/leyas/swe4s_flight_simulator.git
2. Install the required Python dependencies: Navigate to the project directory and install the necessary dependencies by running:

    ```bash
    cd swe4s_flight_simulator

3. Set up the environment using the provided `environment.yml` file:
    If you're using **conda**, you can create a virtual environment with the required dependencies by running:
    ```bash
    conda env create -f environment.yml
    ```

4. Activate the environment:
    ```bash
    conda activate env.yml
    ```

5. You are now ready to run the project!

## Usage

1. After installation, run the GUI file. You will be prompted to input characteristics of the rocket you plan on simulating.

2. Correctly input values that characterize your rocket. 

3. Click "simulate flight path" when ready.

4. Observe flight simulation and record results. 

## Example Output

## Requirements
- Python 3.12
- NumPy
- Matplotlib
- SciPy

