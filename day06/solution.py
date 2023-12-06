import structlog

log = structlog.get_logger()


def part1() -> int:
    return (
        calculate_all_distances(52, 426)
        * calculate_all_distances(94, 1374)
        * calculate_all_distances(75, 1279)
        * calculate_all_distances(94, 1216)
    )


def part2() -> int:
    return calculate_all_distances(52947594, 426137412791216)


def calculate_distance(button_time: int, total_race_time: int) -> int:
    """
    Calculate the distance of a particular button_time. The race time
    is the total time - how long the button is held.
    """
    race_time = total_race_time - button_time
    return (button_time + 1) * (race_time - 1)


def calculate_all_distances(total_race_time: int, record_distance: int) -> int:
    """
    Calculate all distances from 0 to `total_race_time`. Find out how many
    races are further than `record_distance`.
    """
    s = 0
    for button_time in range(0, total_race_time):
        if calculate_distance(button_time, total_race_time) > record_distance:
            s += 1
    return s


if __name__ == "__main__":
    print(part1())
    print(part2())
