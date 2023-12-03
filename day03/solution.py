import math
from typing import Any

import structlog

log = structlog.get_logger()

Row = list[Any]
Grid = list[list[Any]]


def get_part_numbers(row: Row) -> dict[int, int]:
    """
    Extract all the possible part numbers from a row.
    """

    part_numbers = {}
    part_number = ""
    for i, char in enumerate(row):
        try:
            part_number += f"{int(char)}"
        except ValueError:
            if part_number:
                for j in range(len(part_number)):
                    part_numbers[i - j - 1] = int(part_number)
                part_number = ""
    for j in range(len(part_number)):
        part_numbers[i - j - 1] = int(part_number)
    return part_numbers


def find_adjacent_part_numbers(x: int, y: int, grid: Grid) -> set[int]:
    """
    Find a distinct set of part numbers adjacdent to the supplied
    (x, y) in the grid.
    """
    v = set()

    # search row below
    if y + 1 < len(grid):
        part_numbers = get_part_numbers(grid[y + 1])
        if x - 1 >= 0 and x - 1 in part_numbers:
            v.add(part_numbers[x - 1])
        if x in part_numbers:
            v.add(part_numbers[x])
        if x + 1 < len(grid) and x + 1 in part_numbers:
            v.add(part_numbers[x + 1])

    # search current row
    part_numbers = get_part_numbers(grid[y])
    if x - 1 >= 0 and x - 1 in part_numbers:
        v.add(part_numbers[x - 1])
    if x in part_numbers:
        v.add(part_numbers[x])
    if x + 1 < len(grid) and x + 1 in part_numbers:
        v.add(part_numbers[x + 1])

    # search row above
    if y - 1 >= 0:
        part_numbers = get_part_numbers(grid[y - 1])
        if x - 1 >= 0 and x - 1 in part_numbers:
            v.add(part_numbers[x - 1])
        if x in part_numbers:
            v.add(part_numbers[x])
        if x + 1 < len(grid) and x + 1 in part_numbers:
            v.add(part_numbers[x + 1])

    return v


def build_grid() -> Grid:
    """
    Helper function to build the grid.
    """

    grid = []
    with open("puzzle", "r") as f:
        for line in f:
            grid.append(list(line.strip()))
    return grid


def part1() -> int:
    s = 0
    grid = build_grid()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char not in [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                matches = find_adjacent_part_numbers(x, y, grid)
                s += sum(matches)

    return s


def part2() -> int:
    s = 0
    grid = build_grid()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "*":
                matches = find_adjacent_part_numbers(x, y, grid)
                if len(matches) == 2:
                    s += math.prod(matches)

    return s


if __name__ == "__main__":
    print(part1())
    print(part2())
