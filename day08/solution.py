import math
from typing import Any

import structlog

log = structlog.get_logger()


class Node:
    """
    Simple node class with a name and left/right attributes.
    """

    def __init__(self, name: str):
        self.name = name
        self.left: Any = None
        self.right: Any = None


def build_nodes() -> tuple[str, dict[str, Node]]:
    """
    Helper function to build the graph of nodes
    and get the instructions.
    """
    nodes = {}
    with open("puzzle", "r") as f:
        directions = f.readline().strip()
        f.readline()
        for line in f:
            node, leftright = line.strip().split(" = ")
            left, right = leftright.replace("(", "").replace(")", "").split(", ")
            if node not in nodes:
                nodes[node] = Node(node)
            if left not in nodes:
                nodes[left] = Node(left)
            if right not in nodes:
                nodes[right] = Node(right)

            nodes[node].left = nodes[left]
            nodes[node].right = nodes[right]
    return directions, nodes


def part1() -> int:
    steps = 0
    directions, nodes = build_nodes()
    current = nodes["AAA"]
    while current.name != "ZZZ":
        next_direction = directions[steps % len(directions)]
        if next_direction == "L":
            current = current.left
        if next_direction == "R":
            current = current.right
        steps += 1
    return steps


def part2() -> int:
    all_steps = []
    directions, nodes = build_nodes()
    current = [node for name, node in nodes.items() if name.endswith("A")]
    for node in current:
        steps = 0
        while not node.name.endswith("Z"):
            next_direction = directions[steps % len(directions)]
            if next_direction == "L":
                node = node.left
            if next_direction == "R":
                node = node.right
            steps += 1
        all_steps.append(steps)
    return math.lcm(*all_steps)


if __name__ == "__main__":
    print(part1())
    print(part2())
