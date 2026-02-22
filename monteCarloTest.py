import numpy as np
import math
from scipy import stats
from mergeSort import MergeSort

def run_monte_carlo(n, k):
    ms = MergeSort()
    results = []

    for _ in range(k):
        arr = np.random.uniform(0, 1, n)
        metrics = ms.sort(arr)
        results.append(metrics["comparisons"])

    return results

def analyze_results(data):
    mean = np.mean(data)
    variance = np.var(data, ddof=1)
    std_error = stats.sem(data)

    confidence_interval = stats.t.interval(
        0.95,
        len(data) - 1,
        loc=mean,
        scale=std_error
    )

    return mean, variance, confidence_interval

if __name__ == "__main__":
    n = 1000
    k = 200

    data = run_monte_carlo(n, k)
    mean, variance, ci = analyze_results(data)

    theoretical = n * math.log2(n)

    print(f"Input size n = {n}")
    print(f"Trials k = {k}")
    print(f"Empirical Mean Comparisons: {mean:.2f}")
    print(f"Variance: {variance:.2f}")
    print(f"95% Confidence Interval: {ci}")
    print(f"Theoretical n log2(n): {theoretical:.2f}")
    print(f"Ratio (mean / n log n): {mean / theoretical:.4f}")