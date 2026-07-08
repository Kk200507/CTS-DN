"""Week-1 explanation of asymptotic analysis and algorithm growth."""

import math


# =====================================================================
# Asymptotic Notation
# =====================================================================
# Big O gives an upper bound on growth.
# Big Omega gives a lower bound on growth.
# Big Theta gives a tight bound on growth.


def describe_notation() -> None:
    print("Big O: worst-case upper bound")
    print("Big Omega: best-case lower bound")
    print("Big Theta: tight bound when upper and lower match")


# =====================================================================
# Best, Average, and Worst Case
# =====================================================================
# Best case is the fastest possible input.
# Average case is the expected input pattern.
# Worst case is the slowest possible input.


def describe_cases() -> None:
    print("Best case: search finds the item immediately")
    print("Average case: search checks about half the items")
    print("Worst case: search checks every item")


# =====================================================================
# Comparing Example Complexities
# =====================================================================
# These formulas show how work grows as input size increases.


def constant_time(n: int) -> int:
    return 1


def logarithmic_time(n: int) -> int:
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


def linear_time(n: int) -> int:
    return n


def linearithmic_time(n: int) -> int:
    return int(n * math.log2(n)) if n > 1 else 0


def quadratic_time(n: int) -> int:
    return n * n


def compare_examples() -> None:
    sizes = [4, 8, 16]
    print("n | O(1) | O(log n) | O(n) | O(n log n) | O(n^2)")
    print("-" * 55)
    for size in sizes:
        print(
            f"{size:2d} | {constant_time(size):4d} | {logarithmic_time(size):8d} | "
            f"{linear_time(size):4d} | {linearithmic_time(size):10d} | "
            f"{quadratic_time(size):6d}"
        )


def main() -> None:
    print("Asymptotic analysis demo")
    describe_notation()
    print()
    describe_cases()
    print()
    compare_examples()


if __name__ == "__main__":
    main()
