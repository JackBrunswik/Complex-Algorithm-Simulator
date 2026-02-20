import math

class MergeSort:
    def __init__(self):
        self.resetMetrics()

    def resetMetrics(self):
        """Reset operation counters."""
        self.comparisons = 0
        self.array_accesses = 0
        self.assignments = 0

    def sort(self, arr):
        """Public method to run merge sort. Returns a dictionary of metrics."""
        self.resetMetrics()
        arrCopy = list(arr)
        self._mergeSort(arrCopy)
        return {
            "comparisons": self.comparisons,
            "array_accesses": self.array_accesses,
            "assignments": self.assignments,
            "total_comparisons": self.comparisons
        }

    def _mergeSort(self, arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = self._mergeSort(arr[:mid])
        right = self._mergeSort(arr[mid:])

        return self._merge(left, right)

    def _merge(self, left, right):
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            # Count comparison
            self.comparisons += 1
            self.array_accesses += 2

            if left[i] <= right[j]:
                merged.append(left[i])
                self.assignments += 1
                i += 1
            else:
                merged.append(right[j])
                self.assignments += 1
                j += 1

        # Remaining elements
        while i < len(left):
            merged.append(left[i])
            self.array_accesses += 1
            self.assignments += 1
            i += 1

        while j < len(right):
            merged.append(right[j])
            self.array_accesses += 1
            self.assignments += 1
            j += 1

        return merged