# Rocket Flight Simulation Project

## Overview

This project simulates the flight trajectory of a rocket using both **aerodynamic** and **physical** calculations based on user-defined parameters. The goal is to compute the rocket's 1-dimensional flight path (position and velocity) from launch to landing. The simulation accounts for various factors such as airframe properties, motor thrust, drag, gravity, and more.

The project includes two primary calculation modules:
- **AeroCalcs**: Performs aerodynamic calculations (e.g., air density, drag coefficient, center of gravity).
- **PhysCalcs**: Handles the physical simulation of the rocket's flight trajectory using numerical integration (e.g., velocity, position, and mass changes).

## Features

- **Input Rocket Parameters**: Define rocket specifications in a JSON file.
- **Aerodynamic Calculations**: Calculate drag, center of gravity (CG), and other aerodynamic properties.
- **Flight Simulation**: Simulate the rocket's ascent and descent using numerical integration.
- **Trajectory Plotting**: Visualize the rocket's flight path with position and velocity over time.
- **Customizable Material and Motor**: Choose different materials and motors for the rocket to see their effects on performance.

## Project Structure

