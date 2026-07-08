"""Week-1 sorting algorithm examples with clear, beginner-friendly code."""

# =====================================================================
# Bubble Sort
# =====================================================================
# Repeatedly swap adjacent items until the list is sorted.


def bubble_sort(numbers: list[int]) -> list[int]:
    for end in range(len(numbers) - 1, 0, -1):
        for index in range(end):
            if numbers[index] > numbers[index + 1]:
                numbers[index], numbers[index + 1] = (
                    numbers[index + 1],
                    numbers[index],
                )
    return numbers


# =====================================================================
# Insertion Sort
# =====================================================================
# Insert each item into its correct position in the sorted part.


def insertion_sort(numbers: list[int]) -> list[int]:
    for index in range(1, len(numbers)):
        current_value = numbers[index]
        position = index - 1

        while position >= 0 and numbers[position] > current_value:
            numbers[position + 1] = numbers[position]
            position -= 1

        numbers[position + 1] = current_value
    return numbers


# =====================================================================
# Merge Sort
# =====================================================================
# Split the list into halves, sort each half, then merge them.


def merge_sort(numbers: list[int]) -> list[int]:
    if len(numbers) <= 1:
        return numbers

    middle = len(numbers) // 2
    left = merge_sort(numbers[:middle])
    right = merge_sort(numbers[middle:])
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    merged = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


# =====================================================================
# Quick Sort
# =====================================================================
# Choose a pivot, move smaller items left and larger items right.


def quick_sort(numbers: list[int]) -> list[int]:
    if len(numbers) <= 1:
        return numbers

    pivot = numbers[-1]
    smaller = [value for value in numbers[:-1] if value <= pivot]
    larger = [value for value in numbers[:-1] if value > pivot]
    return quick_sort(smaller) + [pivot] + quick_sort(larger)


# =====================================================================
# Heap Sort
# =====================================================================
# Build a max heap and repeatedly move the largest item to the end.


def heapify(numbers: list[int], size: int, root_index: int) -> None:
    largest = root_index
    left_child = 2 * root_index + 1
    right_child = 2 * root_index + 2

    if left_child < size and numbers[left_child] > numbers[largest]:
        largest = left_child
    if right_child < size and numbers[right_child] > numbers[largest]:
        largest = right_child
    if largest != root_index:
        numbers[root_index], numbers[largest] = numbers[largest], numbers[root_index]
        heapify(numbers, size, largest)


def heap_sort(numbers: list[int]) -> list[int]:
    size = len(numbers)

    for index in range(size // 2 - 1, -1, -1):
        heapify(numbers, size, index)

    for end in range(size - 1, 0, -1):
        numbers[0], numbers[end] = numbers[end], numbers[0]
        heapify(numbers, end, 0)

    return numbers


def main() -> None:
    sample = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", sample)
    print("Bubble sort:", bubble_sort(sample.copy()))
    print("Insertion sort:", insertion_sort(sample.copy()))
    print("Merge sort:", merge_sort(sample.copy()))
    print("Quick sort:", quick_sort(sample.copy()))
    print("Heap sort:", heap_sort(sample.copy()))


if __name__ == "__main__":
    main()
