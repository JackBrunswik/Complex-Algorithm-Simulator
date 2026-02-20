import numpy as np
from mergeSort import MergeSort
import math

ms = MergeSort()

for n in [100, 500, 1000, 2000]:
    arr = np.random.uniform(0, 1, n)
    metrics = ms.sort(arr)
    comparisons = metrics["comparisons"]

    theoretical = n * math.log2(n)
    ratio = comparisons / theoretical

    print(f"n={n}")
    print(f"Comparisons: {comparisons}")
    print(f"n log2 n: {int(theoretical)}")
    print(f"Ratio: {ratio:.3f}")
    print("-" * 30)