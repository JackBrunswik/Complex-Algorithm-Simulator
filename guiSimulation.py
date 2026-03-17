import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from kargerMinCut import KargerMinCut

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

        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

    # UI controls
    def create_controls(self):
        """ Creates the left-side control panel:
        - Mode selector
        - Algorithm selector
        - Input parameters
        - Run / Stop buttons """
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        vcmd_pos = (self.root.register(self.validate_positive_int), "%P")
        vcmd_karger = (self.root.register(self.validate_karger_n), "%P")

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
            values=["Randomized Quick Sort", "Random Graph BFS", "Karger Min-Cut"],
            state="readonly"
        )
        self.algorithm_choice.current(0)
        self.algorithm_choice.pack()

        # Monte Carlo parameters
        ttk.Label(control_frame, text="Min n:").pack()
        self.min_n = ttk.Entry(control_frame, validate="key", validatecommand=vcmd_pos)
        self.min_n.insert(0, "10")
        self.min_n.pack()

        ttk.Label(control_frame, text="Max n:").pack()
        self.max_n = ttk.Entry(control_frame, validate="key", validatecommand=vcmd_pos)
        self.max_n.insert(0, "500")
        self.max_n.pack()

        ttk.Label(control_frame, text="Step:").pack()
        self.step = ttk.Entry(control_frame, validate="key", validatecommand=vcmd_pos)
        self.step.insert(0, "10")
        self.step.pack()

        ttk.Label(control_frame, text="Trials (k):").pack()
        self.k_trials = ttk.Entry(control_frame, validate="key", validatecommand=vcmd_pos)
        self.k_trials.insert(0, "100")
        self.k_trials.pack()

        # BFS visualization legend
        self.bfs_legend = ttk.Label(
            control_frame,
            text="BFS Legend\n\nRed = Current\nOrange = Frontier\nBlue = Visited",
            justify="left"
        )
        self.mode_choice.bind("<<ComboboxSelected>>", lambda e: self.update_bfs_legend_visibility())
        self.algorithm_choice.bind("<<ComboboxSelected>>", lambda e: self.update_bfs_legend_visibility())

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

    # Toggle BFS Legend
    def update_bfs_legend_visibility(self):
        algorithm = self.algorithm_choice.get()
        mode = self.mode_choice.get()

        if algorithm == "Random Graph BFS" and mode == "Visualization":
            if not self.bfs_legend.winfo_ismapped():
                self.bfs_legend.pack(pady=(10, 0))
        else:
            if self.bfs_legend.winfo_ismapped():
                self.bfs_legend.pack_forget()

    # Stop sim
    def stop_simulation(self):
        # Sets stop flag to True. All loops check this flag to safely exit early
        self.stop_requested = True

    def exit_program(self):
        # Closes the application window
        self.root.destroy()

    # Plot setup
    def create_plot(self):
        # Creates matplotlib figure embedded inside Tkinter
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def validate_positive_int(self, value):
        # Allow only positive integers
        if value == "":
            return True
        return value.isdigit() and int(value) > 0

    def validate_karger_n(self, value):
        # Karger requires n >= 2
        if value == "":
            return True
        return value.isdigit() and int(value) >= 2

    # BFS visualization
    def visualize_and_run_bfs(self):
        # Generates a connected random graph and animates Breadth-First Search traversal using BFS layers

        self.ax.set_title("Random Graph BFS Traversal")
        n = int(self.min_n.get())
        p = 0.1

        if n > 40:
            print("Visualization limited to n <= 40")
            return

        bfs_sim = RandomGraphBFS(p)
        G = bfs_sim.generate_connected_graph(n)

        pos = nx.spring_layout(G, seed=42)

        visited = set()
        queue = [0]

        visited.add(0)

        # Track node colors
        node_colors = {node: "lightgray" for node in G.nodes()}

        while queue:
            if self.stop_requested:
                break

            current = queue.pop(0)

            # Current node becomes RED
            node_colors[current] = "red"

            self.ax.clear()
            nx.draw(
                G,
                pos,
                ax=self.ax,
                node_color=[node_colors[n] for n in G.nodes()],
                with_labels=True,
                font_size=8,
                node_size=500
            )
            self.bfs_legend.config(text=f"""
            Red = Current
            Orange = Frontier
            Blue = Visited

            Current Node: {current}
            Queue Size: {len(queue)}
            Visited: {len(visited)}
            """)
            self.canvas.draw()
            self.root.update()
            self.root.after(500)

            # Collect ALL neighbors first
            new_neighbors = []

            for neighbor in G.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    new_neighbors.append(neighbor)

            # Highlight them simultaneously (ORANGE)
            for node in new_neighbors:
                node_colors[node] = "orange"

            self.ax.clear()
            nx.draw(
                G,
                pos,
                ax=self.ax,
                node_color=[node_colors[n] for n in G.nodes()],
                with_labels=True,
                font_size=8,
                node_size=500
            )
            self.bfs_legend.config(text=f"""
            Red = Current
            Orange = Frontier
            Blue = Visited

            Current Node: {current}
            Queue Size: {len(queue)}
            Visited: {len(visited)}
            """)
            self.canvas.draw()
            self.root.update()
            self.root.after(500)

            # Mark current node as fully visited (BLUE)
            node_colors[current] = "blue"

            self.ax.clear()
            nx.draw(
                G,
                pos,
                ax=self.ax,
                node_color=[node_colors[n] for n in G.nodes()],
                with_labels=True,
                font_size=8,
                node_size=500
            )
            self.bfs_legend.config(text=f"""
            Red = Current
            Orange = Frontier
            Blue = Visited

            Current Node: {current}
            Queue Size: {len(queue)}
            Visited: {len(visited)}
            """)
            self.canvas.draw()
            self.root.update()
            self.root.after(500)

    # Monte Carlo mode
    def run_monte_carlo(self):
        """ Performs Monte Carlo simulation of Randomized Quick Sort. For each input size n:
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
        variance = []

        for n in n_values:

            if self.stop_requested:
                break

            algorithm = QuickSort()
            results = []

            for _ in range(k):
                arr = np.random.uniform(0, 1, n)
                metrics = algorithm.sort(arr)
                results.append(metrics["comparisons"])

            mean_val = np.mean(results)
            var_val = np.var(results, ddof=1)

            empirical.append(mean_val)
            variance.append(var_val)
            theoretical.append(n * math.log2(n))
            std_dev = np.sqrt(variance[:len(empirical)])

            # Realtime plot update
            self.ax.clear()

            # Empirical mean with error bars (standard deviation)
            self.ax.errorbar(n_values[:len(empirical)], empirical, yerr=std_dev, fmt='o-', capsize=4, label="Empirical Mean + Standard Deviation")

            # Theoretical curve
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
            - Record max tree depth
            - Plot empirical mean vs theoretical 2 * log(n) """
        min_n = int(self.min_n.get())
        max_n = int(self.max_n.get())
        step = int(self.step.get())
        k = int(self.k_trials.get())

        if min_n < 5:
            print("Input Error: Minimum input value must be 5 or greater")
            return

        n_values = list(range(min_n, max_n + 1, step))

        empirical = []
        theoretical = []
        variance = []

        for n in n_values:
            if self.stop_requested:
                break

            bfs_sim = RandomGraphBFS()
            results = []

            for _ in range(k):
                G = nx.connected_watts_strogatz_graph(n, k=4, p=0.1)
                metrics = bfs_sim.run_bfs(G)
                results.append(metrics["max_depth"])

            mean_val = np.mean(results)
            var_val = np.var(results, ddof=1)

            empirical.append(mean_val)
            variance.append(var_val)
            theoretical.append(2 * math.log(n))
            std_dev = np.sqrt(variance[:len(empirical)])

            # Realtime plot update
            self.ax.clear()

            # Empirical mean with error bars (standard deviation)
            self.ax.errorbar(n_values[:len(empirical)], empirical, yerr=std_dev, fmt='o-', capsize=4, label="Empirical Mean + Standard Deviation")

            # Theoretical curve
            self.ax.plot(n_values[:len(theoretical)], theoretical, label="Theoretical 2 log(n)")

            self.ax.set_xlabel("Number of Nodes (n)")
            self.ax.set_ylabel("Tree Depth")
            self.ax.set_title("Monte Carlo Simulation: Random Graph BFS")
            self.ax.legend()

            self.canvas.draw()
            self.root.update()

    def run_karger_monte_carlo(self):
        min_n = int(self.min_n.get())
        max_n = int(self.max_n.get())
        step = int(self.step.get())
        k = int(self.k_trials.get())

        n_values = list(range(min_n, max_n + 1, step))

        empirical = []
        theoretical = []
        variance = []

        karger = KargerMinCut()

        for n in n_values:
            if self.stop_requested:
                break

            # Generate one graph for this n
            G = karger.generate_graph(n)

            # Compute true minimum cut once
            true_cut = len(nx.minimum_edge_cut(G))

            success_count = 0

            for _ in range(k):
                result = karger.run_karger(G)

                if result["cut_size"] == true_cut:
                    success_count += 1

            success_probability = success_count / k

            variance_val = success_probability * (1 - success_probability)
            variance.append(variance_val)

            empirical.append(success_probability)
            theoretical.append(2 / (n * (n - 1)))
            std_dev = np.sqrt(variance[:len(empirical)])

            # Realtime plot update
            self.ax.clear()

            # Empirical mean with error bars (standard deviation)
            self.ax.errorbar(n_values[:len(empirical)], empirical, yerr=std_dev, fmt='o-', capsize=4, label="Empirical Mean + Standard Deviation")

            # Theoretical curve
            self.ax.plot(n_values[:len(theoretical)], theoretical, label="Theoretical n log n")

            self.ax.set_xlabel("Number of Nodes (n)")
            self.ax.set_ylabel("Probability of Finding Min-Cut")

            self.ax.set_title("Monte Carlo Simulation: Karger's Min-Cut")

            self.ax.legend()

            self.canvas.draw()
            self.root.update()

    def visualize_karger(self):
        n = int(self.min_n.get())

        if n > 25:
            print("Visualization limited to n <= 25")
            return

        karger = KargerMinCut()
        G = karger.generate_graph(n)

        pos = nx.spring_layout(G, seed=42)

        generator = karger.contraction_generator(G)

        for state, edge in generator:
            if self.stop_requested:
                break

            self.ax.clear()

            # Default node colors
            node_colors = ["lightblue" for _ in state.nodes()]

            # Highlight nodes that will be merged
            if edge is not None:
                u, v = edge

                node_colors = [
                    "red" if node == u or node == v else "lightblue"
                    for node in state.nodes()
                ]

            nx.draw(
                state,
                pos,
                ax=self.ax,
                node_color=node_colors,
                edge_color="gray",
                with_labels=True,
                node_size=500
            )

            # Highlight the edge being contracted
            if edge is not None and state.has_edge(*edge):
                nx.draw_networkx_edges(
                    state,
                    pos,
                    edgelist=[edge],
                    edge_color="red",
                    width=3,
                    ax=self.ax
                )
            self.ax.set_title("Karger's Min-Cut Contraction")
            self.canvas.draw()
            self.root.update()
            self.root.after(800)

    # Sort visualization mode
    def visualize_sort(self):
        # Animates a single randomized Quick Sort trial. Highlights currently active elements during swaps.
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

        if algorithm_name == "Karger Min-Cut":
            if int(self.min_n.get()) < 2:
                print("Karger Min-Cut requires n >= 2")
                return

        if algorithm_name == "Random Graph BFS":
            if mode == "Monte Carlo":
                self.run_bfs_monte_carlo()
            else:
                self.visualize_and_run_bfs()
            return

        if algorithm_name == "Karger Min-Cut":
            if mode == "Monte Carlo":
                self.run_karger_monte_carlo()
            else:
                self.visualize_karger()
            return

        # Otherwise: QuickSort
        if mode == "Monte Carlo":
            self.run_monte_carlo()
        else:
            self.visualize_sort()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationGUI(root)
    # Hides unimportant error message when stopping the program in the IDE
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass