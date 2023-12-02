import structlog

log = structlog.get_logger()

D = {"red": 12, "green": 13, "blue": 14}


def part1() -> int:
    s = 0
    with open("puzzle", "r") as f:
        for line in f:
            id, games = line.strip().split(": ")
            id = int(id.split(" ")[-1])
            valid = True
            for game in games.split("; "):
                for pull in game.split(", "):
                    n, color = pull.split(" ")
                    if int(n) > D[color]:
                        valid = False
                        break
            if valid:
                s += id

    return s


def part2() -> int:
    s = 0
    with open("puzzle", "r") as f:
        for line in f:
            id, games = line.strip().split(": ")
            id = int(id.split(" ")[-1])
            d = {}
            for game in games.split("; "):
                for pull in game.split(", "):
                    n, color = pull.split(" ")
                    d[color] = max(d.get(color, 0), int(n))
            s += d["red"] * d["green"] * d["blue"]
    return s


if __name__ == "__main__":
    print(part1())
    print(part2())
