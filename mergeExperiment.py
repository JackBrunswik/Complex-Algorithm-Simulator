import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats
from mergeSort import MergeSort

def run_trials(n, k):
    ms = MergeSort()
    results = []

    for _ in range(k):
        arr = np.random.uniform(0, 1, n)
        metrics = ms.sort(arr)
        results.append(metrics["comparisons"])

    return results

def analyze(data):
    mean = np.mean(data)
    variance = np.var(data, ddof=1)
    std_error = stats.sem(data)

    ci = stats.t.interval(
        0.95,
        len(data) - 1,
        loc=mean,
        scale=std_error
    )

    return mean, variance, ci

if __name__ == "__main__":
    n_values = [100, 500, 1000, 2000, 5000]
    k = 200

    empirical_means = []
    theoretical_values = []
    lower_bounds = []
    upper_bounds = []

    # Turn on interactive mode
    plt.ion()
    fig, ax = plt.subplots()

    for n in n_values:
        print(f"Running n = {n}")

        data = run_trials(n, k)
        mean, variance, ci = analyze(data)
        theoretical = n * math.log2(n)

        empirical_means.append(mean)
        theoretical_values.append(theoretical)
        lower_bounds.append(ci[0])
        upper_bounds.append(ci[1])

        # Clear axis
        ax.clear()

        # Plot updated results
        ax.plot(n_values[:len(empirical_means)], empirical_means)
        ax.plot(n_values[:len(theoretical_values)], theoretical_values)

        ax.fill_between(
            n_values[:len(lower_bounds)],
            lower_bounds,
            upper_bounds,
            alpha=0.3
        )

        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Comparisons")
        ax.set_title("Real-Time Monte Carlo Convergence")

        plt.pause(0.5)

    plt.ioff()
    plt.show()