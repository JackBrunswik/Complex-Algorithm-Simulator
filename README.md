# Complex Algorithm Simulator Overview

A stochastic simulation and visualization tool for analyzing and comparing algorithm behavior under varying input sizes.

This project integrates Monte Carlo experimentation with real-time algorithm visualization, allowing users to study both empirical complexity and step-by-step execution within an interactive framework.

## Current Features

### Monte Carlo Mode
- Runs repeated randomized trials for varying input sizes
- Computes empirical mean comparisons
- Plots performance growth
- Compares empirical results against theoretical O(n log n)

### Visualization Mode
- Real-time array graph animation of Quick Sort
- Displays array transformations during sorting

- For Random Graph BFS:
  - Generates a connected random graph
  - Labels all nodes numerically
  - Animates breadth-first traversal in real-time

## Possible Future Features

- Add Karger's Min-Cut algorithm
- Upgrade simulation depth:
  - Variance tracking
  - Add Histogram mode
  - Parameter sweeps

## Algorithms Implemented

- Random Quick Sort — Expected O(n log n)
- Random Graph Breadth-First Search

## Technologies Used

- Python
- NumPy
- SciPy
- Matplotlib
- NetworkX
- Tkinter (GUI framework)

## Installation

### Make sure Python 3.10 or newer is installed:

python --version

### Clone the repository:

git clone https://github.com/JackBrunswik/Complex-Algorithm-Simulator.git

cd Complex-Algorithm-Simulator

### Install dependencies:

pip install -r requirements.txt

### Run the application:

python guiSimulation.py

## Expected Outcome/Behavior

When the program is launched, a graphical user interface window opens that allows the user to select a simulation mode, choose an algorithm, and configure input parameters such as input size and number of trials.

The program currently operates in two main modes:

Monte Carlo Mode:
The simulator runs multiple randomized trials of the selected algorithm across a range of input sizes. For each input size, it computes the average of a measured performance metric (e.g., comparisons for Quick Sort or edges examined for BFS). A real-time graph is displayed showing empirical results alongside a theoretical growth curve (e.g., n logn for QuickSort or expected edges for random graphs). The graph updates progressively as the simulation runs.

Visualization Mode:
The simulator executes a single representative randomized trial and visually animates the algorithm’s behavior. For Quick Sort, array elements are displayed as bars, and active elements are highlighted as sorting progresses. For Random Graph BFS, a randomly generated graph is displayed, and nodes are visually marked as they are visited during traversal.

The program allows the user to stop simulations at any time using the Stop button. No files are written by default, all results are displayed interactively within the GUI.

## Architecture Overview

### Main Components
- Simulation Controller (GUI):
Acts as the central controller of the application, handling user input, managing simulation modes (Monte Carlo and Visualization), coordinating algorithm execution, and rending plots and animations.
 
- Quick Sort:
Implements the randomized Quick Sort algorithm, executes stochastic trials, tracks performance metrics, such as comparisons, and supports step-by-step visualization through a generator.
 
- Random Graph BFS:
Generates random graphs using the Erdos-Renyi model and performs Breadth-First Search, collecting metrics such as edges examined and tree height for Monte Carlo analysis.
 
- Visualization (Matplotlib and NetworkX):
Provides real-time plotting of empirical results and animated visual representations of sorting and graph traveral processes.
 
- Metrics Collection:
Each algorithm internally records and returns structured performance data, which is aggregated during Monte Carlo simulations for statistical analysis.

### Architectural Design Changes
Compared to the original UML design, the system has changed from a generalized event-driven simulation engine to a Monte Carlo-based stochastic algorithm simulator. The original simulation concept is implemented by the GUI, but without event queues or discrete-time scheduling, as the project shifted toward trial-based empirical analysis rather than time-stepped simulation. The abstract Algorithm concept is preserved conceptually through the independent algorithm classes, though no formal base class is currently implemented. Data structures such as arrays and graphs are managed internally by their respective algorithms rather than through a separate abstraction layer. Similarly, metric collection is embedded within each algorithm class and returned as structured dictionaries instead of being handled by a standalone metrics collector. These architectural changes were made to reduce unnecessary abstraction and better align the system with a more refined goal: simulating and analyzing algorithm behavior through Monte Carlo experimentation and real-time visualization.

Also, Merge Sort was removed entirely considering that it's a deterministic algorithm, which is not good for simulating in this case.
