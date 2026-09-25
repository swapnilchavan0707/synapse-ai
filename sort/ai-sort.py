class AdaptiveSortingAgent:
    def __init__(self, fallback_threshold=16):
        self.fallback_threshold = fallback_threshold
        self.telemetry = {"quick_sort_calls": 0, "merge_sort_calls": 0}

    def _calculate_entropy_heuristic(self, arr):
        # Intelligent metric to check local disorder or partition cost
        if len(arr) <= 1:
            return 0.0
        inversions = sum(1 for i in range(len(arr) - 1) if arr[i] > arr[i + 1])
        return inversions / (len(arr) - 1)

    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _merge_sort(self, arr):
        self.telemetry["merge_sort_calls"] += 1
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        return self._merge(left, right)

    def optimize_and_sort(self, arr):
        if len(arr) <= 1:
            return arr

        # Agent decision boundary based on size and entropy check
        disorder_score = self._calculate_entropy_heuristic(arr)
        if len(arr) <= self.fallback_threshold or disorder_score < 0.2:
            return self._merge_sort(arr)

        self.telemetry["quick_sort_calls"] += 1
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return self.optimize_and_sort(left) + middle + self.optimize_and_sort(right)

if __name__ == "__main__":
    agent = AdaptiveSortingAgent(fallback_threshold=8)
    data_stream = [42, 12, 99, 18, 5, 63, 22, 10, 85, 3]
    sorted_stream = agent.optimize_and_sort(data_stream)
    print("Agent Sorted Data:", sorted_stream)
    print("Execution Telemetry:", agent.telemetry)