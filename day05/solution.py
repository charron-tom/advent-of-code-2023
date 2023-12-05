from typing import Callable, TypeVar

import structlog

log = structlog.get_logger()
T = TypeVar("T")
Range = tuple[int, int]
Mapping = tuple[int, int, int]


def part1() -> int:
    transforms, _seeds = get_transforms(get_mapper)
    seeds = [int(seed) for seed in _seeds]
    item = "seed"
    while item != "location":
        next_item, mapper = transforms[item]
        seeds = [mapper(n) for n in seeds]
        item = next_item
    return min(seeds)


def part2() -> int:
    transforms, _seeds = get_transforms(get_range_mapper)
    seeds = [(int(_seeds[i]), int(_seeds[i + 1])) for i in range(0, len(_seeds) - 1, 2)]
    item = "seed"
    while item != "location":
        next_item, mapper = transforms[item]
        seeds = mapper(seeds)
        item = next_item
    return min([seed[0] for seed in seeds])


def get_transforms(
    mapper_fn: Callable[[list[Mapping]], T]
) -> tuple[dict[str, tuple[str, T]], list[str]]:
    """
    Parse the input file and return a dictionary
    of transform functions and the initial seeds.
    """
    transforms: dict[str, tuple[str, T]] = {}
    with open("puzzle", "r") as f:
        seed_data = f.readline().split("seeds: ")[-1].split()
        f.readline()
        src = ""
        dst = ""
        mappings: list[Mapping] = []
        for line in f:
            if "map" in line:
                src, rest = line.strip().split("-to-")
                dst = rest.split()[0]
            elif not line.strip():
                transforms[src] = (dst, mapper_fn(mappings))
                mappings = []
            else:
                src_start, dst_start, length = line.strip().split()
                mappings.append((int(src_start), int(dst_start), int(length)))
        transforms[src] = (dst, mapper_fn(mappings))
    return transforms, seed_data


def get_mapper(mappings: list[Mapping]) -> Callable[[int], int]:
    """
    Build a mapper function for part 1. The mapper function takes
    a single integer and returns an integer in the destination range.
    """

    def map_fn(n: int) -> int:
        for dst_start, src_start, length in mappings:
            offset = dst_start - src_start
            if n >= src_start and n < src_start + length:
                return n + offset
        return n

    return map_fn


def get_range_mapper(mappings: list[Mapping]) -> Callable[[list[Range]], list[Range]]:
    """
    Build a mapper function for part 2. The mapper
    takes a range and recursively maps it to the destination ranges.
    """

    def map_range(r: list[Range]) -> list[Range]:
        mapped = []
        for range_start, range_length in r:
            for dst_start, src_start, length in mappings:
                offset = dst_start - src_start
                if range_start >= src_start and range_start < src_start + length:
                    overlap_size = min(range_length, src_start + length - range_start)
                    mapped.append((range_start + offset, overlap_size))
                    if range_length != overlap_size:
                        mapped += map_range(
                            [(range_start + overlap_size, range_length - overlap_size)]
                        )
        return mapped

    return map_range


if __name__ == "__main__":
    print(part1())
    print(part2())
