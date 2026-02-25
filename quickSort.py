import random

class QuickSort:
    def __init__(self):
        self.reset_metrics()

    def reset_metrics(self):
        self.comparisons = 0

    def sort(self, arr):
        self.reset_metrics()
        arr_copy = list(arr)
        self.quick_Sort(arr_copy, 0, len(arr_copy) - 1)
        return {"comparisons": self.comparisons}

    def quick_Sort(self, arr, low, high):
        if low < high:
            pivot_index = self._random_partition(arr, low, high)
            self.quick_Sort(arr, low, pivot_index - 1)
            self.quick_Sort(arr, pivot_index + 1, high)

    def sort_generator(self, arr):
        arr = arr.copy()
        yield from self.quick_sort_generator(arr, 0, len(arr) - 1)
        yield arr, []

    def quick_sort_generator(self, arr, low, high):
        if low < high:
            pivot_index = yield from self.partition_generator(arr, low, high)
            yield from self.quick_sort_generator(arr, low, pivot_index - 1)
            yield from self.quick_sort_generator(arr, pivot_index + 1, high)

    def partition_generator(self, arr, low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr.copy(), [i, j]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield arr.copy(), [i + 1, high]

        return i + 1

    def _random_partition(self, arr, low, high):
        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

        return self._partition(arr, low, high)

    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1