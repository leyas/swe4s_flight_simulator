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
   git clone https://github.com/leyas/swe4s_flight_simulator.git
2. Install the required Python dependencies: Navigate to the project directory and install the necessary dependencies by running:

    ```bash
    pip install -r requirements.txt

3. Ensure you have the necessary files: list the contents of your remote repository and ensure the list matches those present here on the webpage 

## Usage

## Requirements
Python 3.x
NumPy
Matplotlib
SciPy

