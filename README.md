# Complex Algorithm Simulator Overview

A stochastic simulation and visualization tool for analyzing and comparing algorithm behavior under varying input sizes.

This project integrates Monte Carlo experimentation with real-time algorithm visualization, allowing users to study both empirical complexity and step-by-step execution within an interactive framework.

## Features

### Monte Carlo Mode
- Runs repeated randomized trials for varying input sizes
- Computes empirical mean comparisons
- Plots performance growth
- Compares empirical results against theoretical results

### Visualization Mode
- Real-time graph animation of a single trial for visual representation
- Displays array transformations during sorting

### Random Graph BFS
- Generates a connected random graph
- Labels all nodes numerically
- Color-coordinated nodes for easier understanding of node phases
- Animates breadth-first traversal in real time

## Algorithms Implemented

- Quick Sort
- Random Graph Breadth-First Search
- Karger's Min-Cut

## Technologies Used

- Python
- NumPy
- SciPy
- Matplotlib
- NetworkX
- Tkinter (GUI framework)

## Installation

Clone the repository:
- git clone https://github.com/JackBrunswik/Complex-Algorithm-Simulator.git  
- cd Complex-Algorithm-Simulator

Install dependencies:
- pip install -r requirements.txt  

Run the application:
- python guiSimulation.py
