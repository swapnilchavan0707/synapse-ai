def merge(left, right):
    # Merge two sorted lists into a single sorted list
    sorted_result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_result.append(left[i])
            i += 1
        else:
            sorted_result.append(right[j])
            j += 1
    sorted_result.extend(left[i:])
    sorted_result.extend(right[j:])
    return sorted_result


def merge_sort(arr):
    # Standard Merge sort implementation
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def hybrid_sort(arr, threshold=16):
    # Hybrid sorting using Quick sort partition + Merge sort fallback
    if len(arr) <= 1:
        return arr

    # Use Merge sort for small sub-arrays below the threshold
    if len(arr) <= threshold:
        return merge_sort(arr)

    # Use Quick sort partitioning for larger arrays
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    # Recursively sort partitions
    return hybrid_sort(left, threshold) + middle + hybrid_sort(right, threshold)


if __name__ == "__main__":
    sample_data = [38, 27, 43, 3, 9, 82, 10, 19, 25, 6, 11]
    sorted_data = hybrid_sort(sample_data, threshold=4)
    print("Sorted array:", sorted_data)
