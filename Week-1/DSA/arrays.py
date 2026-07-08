"""Week-1 array operations examples with simple time complexity notes."""

# =====================================================================
# Traversal
# =====================================================================
# Visiting every element in an array takes O(n) time.


def traverse_array(values: list[int]) -> None:
    for index, value in enumerate(values):
        print(f"Index {index}: {value}")


# =====================================================================
# Searching
# =====================================================================
# Searching through an unsorted array takes O(n) time.


def search_element(values: list[int], target: int) -> int:
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


# =====================================================================
# Insertion
# =====================================================================
# Inserting into the middle of an array may shift elements, so it is O(n).


def insert_element(values: list[int], index: int, value: int) -> list[int]:
    values.insert(index, value)
    return values


# =====================================================================
# Deletion
# =====================================================================
# Deleting from an array may also shift elements, so it is O(n).


def delete_element(values: list[int], value: int) -> list[int]:
    if value in values:
        values.remove(value)
    return values


def main() -> None:
    numbers = [10, 20, 30, 40, 50]
    print("Traversal demo")
    traverse_array(numbers)

    print("\nSearching demo")
    print("Index of 30:", search_element(numbers, 30))
    print("Index of 99:", search_element(numbers, 99))

    print("\nInsertion demo")
    print(insert_element(numbers.copy(), 2, 25))

    print("\nDeletion demo")
    print(delete_element(numbers.copy(), 30))

    print("\nComplexity notes")
    print("Traversal: O(n)")
    print("Searching unsorted array: O(n)")
    print("Insertion in middle: O(n)")
    print("Deletion by value: O(n)")


if __name__ == "__main__":
    main()
