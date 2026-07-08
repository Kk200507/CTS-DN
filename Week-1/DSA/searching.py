"""Week-1 searching algorithm examples with straightforward Python code."""

# =====================================================================
# Linear Search
# =====================================================================
# Check each element one by one.


def linear_search(values: list[int], target: int) -> int:
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


# =====================================================================
# Binary Search
# =====================================================================
# Repeatedly divide a sorted list in half.


def binary_search(values: list[int], target: int) -> int:
    left = 0
    right = len(values) - 1

    while left <= right:
        middle = (left + right) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1


def main() -> None:
    numbers = [5, 12, 18, 21, 35, 48, 60]
    print("Linear search demo")
    print("Index of 21:", linear_search(numbers, 21))
    print("Index of 99:", linear_search(numbers, 99))

    print("\nBinary search demo")
    print("Index of 35:", binary_search(numbers, 35))
    print("Index of 99:", binary_search(numbers, 99))


if __name__ == "__main__":
    main()
