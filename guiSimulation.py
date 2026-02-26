import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

# Import algorithms
from quickSort import QuickSort
from randomGraphBFS import RandomGraphBFS

class SimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stochastic Algorithm Simulation")

        # Flag used to stop running simulations
        self.stop_requested = False

        self.create_controls()
        self.create_plot()

    # UI controls
    def create_controls(self):
        """ Creates the left-side control panel:
        - Mode selector
        - Algorithm selector
        - Input parameters
        - Run / Stop buttons """
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Mode selection
        ttk.Label(control_frame, text="Mode:").pack()
        self.mode_choice = ttk.Combobox(
            control_frame,
            values=["Monte Carlo", "Visualization"],
            state="readonly"
        )
        self.mode_choice.current(0)
        self.mode_choice.pack()

        # Algorithm selection
        ttk.Label(control_frame, text="Algorithm:").pack()
        self.algorithm_choice = ttk.Combobox(
            control_frame,
            values=["Randomized Quick Sort", "Random Graph BFS"],
            state="readonly"
        )
        self.algorithm_choice.current(0)
        self.algorithm_choice.pack()

        # Monte Carlo parameters
        ttk.Label(control_frame, text="Min n:").pack()
        self.min_n = ttk.Entry(control_frame)
        self.min_n.insert(0, "10")
        self.min_n.pack()

        ttk.Label(control_frame, text="Max n:").pack()
        self.max_n = ttk.Entry(control_frame)
        self.max_n.insert(0, "500")
        self.max_n.pack()

        ttk.Label(control_frame, text="Step:").pack()
        self.step = ttk.Entry(control_frame)
        self.step.insert(0, "10")
        self.step.pack()

        ttk.Label(control_frame, text="Trials (k):").pack()
        self.k_trials = ttk.Entry(control_frame)
        self.k_trials.insert(0, "50")
        self.k_trials.pack()

        # Run button
        self.run_button = ttk.Button(
            control_frame,
            text="Run Simulation",
            command=self.run_simulation
        )
        self.run_button.pack(pady=5)

        # Stop button
        self.stop_button = ttk.Button(
            control_frame,
            text="Stop",
            command=self.stop_simulation
        )
        self.stop_button.pack(pady=5)

    # Stop sim
    def stop_simulation(self):
        """ Sets stop flag to True.
        All loops check this flag to safely exit early. """
        self.stop_requested = True

    # Plot setup
    def create_plot(self):
        """ Creates matplotlib figure embedded inside Tkinter. """
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # BFS visualization
    def visualize_and_run_bfs(self):
        """ Generates a connected random graph and animates
        Breadth-First Search traversal in real time. """
        n = int(self.min_n.get())
        p = 0.1  # Edge probability

        # Limit visualization size for clarity
        if n > 40:
            print("Visualization limited to n <= 40")
            return

        bfs_sim = RandomGraphBFS(p)
        G = bfs_sim.generate_connected_graph(n)

        pos = nx.spring_layout(G, seed=42)

        visited = set()
        queue = [0]
        visited.add(0)

        self.ax.clear()

        while queue:

            if self.stop_requested:
                break

            current = queue.pop(0)

            self.ax.clear()

            # Color visited nodes red
            node_colors = [
                "red" if node in visited else "lightblue"
                for node in G.nodes()
            ]
            nx.draw(
                G,
                pos,
                ax=self.ax,
                node_color=node_colors,
                with_labels=True,
                font_size=8,
                node_size=500
            )
            self.ax.set_title("Connected Random Graph BFS Traversal")

            self.canvas.draw()
            self.root.update()
            self.root.after(500)  # 500ms delay

            # Add unvisited neighbors to queue
            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    # Monte Carlo mode
    def run_monte_carlo(self):
        """ Performs Monte Carlo simulation of Randomized Quick Sort.
        For each input size n:
            - Run k randomized trials
            - Compute mean comparison count
            - Plot empirical vs theoretical O(n log n) """
        min_n = int(self.min_n.get())
        max_n = int(self.max_n.get())
        step = int(self.step.get())
        k = int(self.k_trials.get())

        n_values = list(range(min_n, max_n + 1, step))

        empirical = []
        theoretical = []

        for n in n_values:

            if self.stop_requested:
                break

            algorithm = QuickSort()
            results = []

            for _ in range(k):
                arr = np.random.uniform(0, 1, n)
                metrics = algorithm.sort(arr)
                results.append(metrics["comparisons"])

            empirical.append(np.mean(results))
            theoretical.append(n * math.log2(n))

            # Realtime redraw (original behavior)
            self.ax.clear()
            self.ax.plot(n_values[:len(empirical)], empirical, label="Empirical")
            self.ax.plot(n_values[:len(theoretical)], theoretical, label="Theoretical n log n")

            self.ax.set_xlabel("Input Size (n)")
            self.ax.set_ylabel("Comparisons")
            self.ax.set_title("Monte Carlo Simulation: Randomized Quick Sort")
            self.ax.legend()

            self.canvas.draw()
            self.root.update()

    def run_bfs_monte_carlo(self):
        """ Monte Carlo simulation for Random Graph BFS.
        For each input size n:
            - Generate k random connected graphs
            - Run BFS
            - Record edges examined
            - Plot empirical mean vs theoretical expected edges """
        min_n = int(self.min_n.get())
        max_n = int(self.max_n.get())
        step = int(self.step.get())
        k = int(self.k_trials.get())

        p = 0.1
        n_values = list(range(min_n, max_n + 1, step))

        empirical = []
        theoretical = []

        for n in n_values:

            if self.stop_requested:
                break

            bfs_sim = RandomGraphBFS(p)
            results = []

            for _ in range(k):
                G = bfs_sim.generate_connected_graph(n)
                metrics = bfs_sim.run_bfs(G)
                results.append(metrics["edges_examined"])

            empirical.append(np.mean(results))
            theoretical.append(p * n * (n - 1) / 2)

            # Realtime redraw (original behavior)
            self.ax.clear()
            self.ax.plot(n_values[:len(empirical)], empirical, label="Empirical")
            self.ax.plot(n_values[:len(theoretical)], theoretical, label="Theoretical Expected Edges")

            self.ax.set_xlabel("Number of Nodes (n)")
            self.ax.set_ylabel("Edges Examined")
            self.ax.set_title("Monte Carlo Simulation: Random Graph BFS")
            self.ax.legend()

            self.canvas.draw()
            self.root.update()

    # Sort visualization mode
    def visualize_sort(self):
        """ Animates a single randomized Quick Sort trial.
        Highlights currently active elements during swaps. """
        n = int(self.max_n.get())
        arr = np.random.randint(1, 100, n)

        self.ax.clear()
        bars = self.ax.bar(range(len(arr)), arr)

        self.ax.set_title("Randomized Quick Sort — Single Trial")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")

        self.canvas.draw()
        self.root.update()

        generator = QuickSort().sort_generator(arr)

        for state, highlight in generator:

            if self.stop_requested:
                break

            for index, (bar, height) in enumerate(zip(bars, state)):
                bar.set_height(height)

                # Highlight active bars
                if index in highlight:
                    bar.set_color("red")
                else:
                    bar.set_color("lightblue")

            self.canvas.draw()
            self.root.update()
            self.root.after(50)  # Animation speed (ms)

    def run_simulation(self):

        self.stop_requested = False

        algorithm_name = self.algorithm_choice.get()
        mode = self.mode_choice.get()

        if algorithm_name == "Random Graph BFS":

            if mode == "Monte Carlo":
                self.run_bfs_monte_carlo()
            else:
                self.visualize_and_run_bfs()

            return

        # Otherwise: QuickSort
        if mode == "Monte Carlo":
            self.run_monte_carlo()
        else:
            self.visualize_sort()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()