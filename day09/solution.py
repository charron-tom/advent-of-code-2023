import structlog

log = structlog.get_logger()


def gen_next_row(row: list[int]) -> list[int]:
    """
    Compute the next row from the current row
    by doing pairwise substraction. The new row will
    always have 1 less item than the current row.
    """
    next_row = []
    for i in range(1, len(row)):
        next_row.append(row[i] - row[i - 1])
    return next_row


def part1() -> int:
    s = 0
    with open("puzzle", "r") as f:
        for line in f:
            rows = [[int(x) for x in line.strip().split()]]
            while any(rows[-1]):
                rows.append(gen_next_row(rows[-1]))

            # reverse rows so we start at the pyramid and work up
            rows.reverse()
            for i, row in enumerate(rows):
                if i == 0:
                    row.append(0)
                else:
                    row.append(row[-1] + rows[i - 1][-1])
            s += rows[-1][-1]
    return s


def part2() -> int:
    s = 0
    with open("puzzle", "r") as f:
        for line in f:
            rows = [[int(x) for x in line.strip().split()]]
            while any(rows[-1]):
                rows.append(gen_next_row(rows[-1]))

            # reverse rows so we start at the pyramid and work up
            rows.reverse()
            for i, row in enumerate(rows):
                if i == 0:
                    row.insert(0, 0)
                else:
                    row.insert(0, row[0] - rows[i - 1][0])
            s += rows[-1][0]
    return s


if __name__ == "__main__":
    print(part1())
    print(part2())
