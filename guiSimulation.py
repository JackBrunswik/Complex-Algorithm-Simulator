import tkinter as tk
from tkinter import ttk
import numpy as np
import math
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from mergeSort import MergeSort
from quickSort import QuickSort

from mergeSort import MergeSort


class SimulationGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Stochastic Algorithm Simulation")

        self.stop_requested = False

        self.create_controls()
        self.create_plot()

    # UI controls
    def create_controls(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Label(control_frame, text="Algorithm:").pack()

        self.algorithm_choice = ttk.Combobox(
            control_frame,
            values=["Merge Sort", "Quick Sort"],
            state="readonly"
        )
        self.algorithm_choice.current(0)
        self.algorithm_choice.pack()

        ttk.Label(control_frame, text="Min n:").pack()
        self.min_n = ttk.Entry(control_frame)
        self.min_n.insert(0, "100")
        self.min_n.pack()

        ttk.Label(control_frame, text="Max n:").pack()
        self.max_n = ttk.Entry(control_frame)
        self.max_n.insert(0, "2000")
        self.max_n.pack()

        ttk.Label(control_frame, text="Step:").pack()
        self.step = ttk.Entry(control_frame)
        self.step.insert(0, "10")
        self.step.pack()

        ttk.Label(control_frame, text="Trials (k):").pack()
        self.k_trials = ttk.Entry(control_frame)
        self.k_trials.insert(0, "100")
        self.k_trials.pack()

        self.run_button = ttk.Button(
            control_frame,
            text="Run Simulation",
            command=self.run_simulation
        )
        self.run_button.pack(pady=5)

        self.stop_button = ttk.Button(
            control_frame,
            text="Stop",
            command=self.stop_simulation
        )
        self.stop_button.pack(pady=5)

    # Stop simulation
    def stop_simulation(self):
        self.stop_requested = True

    # Plot setup
    def create_plot(self):
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Monte Carlo
    def run_trials(self, n, k):

        if self.algorithm_choice.get() == "Merge Sort":
            algorithm = MergeSort()
        else:
            algorithm = QuickSort()

        results = []

        for _ in range(k):
            if self.stop_requested:
                break

            arr = np.random.uniform(0, 1, n)
            metrics = algorithm.sort(arr)
            results.append(metrics["comparisons"])

            self.root.update()  # keep GUI responsive

        return results

    # Simulation runner
    def run_simulation(self):

        # Reset stop flag at start
        self.stop_requested = False

        # Read user inputs
        min_n = int(self.min_n.get())
        max_n = int(self.max_n.get())
        step = int(self.step.get())
        k = int(self.k_trials.get())

        n_values = list(range(min_n, max_n + 1, step))

        empirical = []
        theoretical = []
        lower = []
        upper = []

        # Clear previous plot
        self.ax.clear()

        for n in n_values:

            # Check if stop was requested
            if self.stop_requested:
                print("Simulation stopped by user.")
                break

            # Run Monte Carlo trials
            data = self.run_trials(n, k)

            # If stopped during trials, exit safely
            if self.stop_requested or not data:
                print("Simulation stopped during trials.")
                break

            # Analyze results
            mean, variance, ci = self.analyze(data)

            empirical.append(mean)
            theoretical.append(n * math.log2(n))
            lower.append(ci[0])
            upper.append(ci[1])

            # Update Plot in Real Time
            self.ax.clear()

            self.ax.plot(n_values[:len(empirical)], empirical, label="Empirical Mean")
            self.ax.plot(n_values[:len(theoretical)], theoretical, label="Theoretical n log n")

            self.ax.fill_between(
                n_values[:len(lower)],
                lower,
                upper,
                alpha=0.3,
                label="95% CI"
            )

            self.ax.set_xlabel("Input Size (n)")
            self.ax.set_ylabel("Comparisons")
            self.ax.set_title("Monte Carlo Algorithm Simulation")
            self.ax.legend()

            self.canvas.draw()

            # Allow GUI to process events
            self.root.update()

        print("Simulation finished.")

    def analyze(self, data):

        """ Performs statistical analysis on Monte Carlo trial results.

        Returns:
            mean (float)
            variance (float)
            confidence_interval (tuple) """

        mean = np.mean(data)

        # Sample variance (unbiased estimator)
        variance = np.var(data, ddof=1)

        # Standard error of the mean
        std_error = stats.sem(data)

        # 95% confidence interval using t-distribution
        ci = stats.t.interval(
            confidence=0.95,
            df=len(data) - 1,
            loc=mean,
            scale=std_error
        )
        return mean, variance, ci

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationGUI(root)
    root.mainloop()