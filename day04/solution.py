import structlog

log = structlog.get_logger()


def part1() -> int:
    s = 0
    with open("puzzle", "r") as f:
        for line in f:
            _, cards = line.strip().split(": ")
            winning, numbers = cards.split(" | ")
            w = set([int(n) for n in winning.split()])
            n = set([int(i) for i in numbers.split()])
            exp = len(n.intersection(w)) - 1
            if exp >= 0:
                s += 2**exp
    return s


def part2() -> int:
    copies = {}
    with open("puzzle", "r") as f:
        for line in f:
            card, cards = line.strip().split(": ")
            id = int(card.split("Card ")[-1])
            winning, numbers = cards.split(" | ")
            w = set([int(n) for n in winning.split()])
            n = set([int(i) for i in numbers.split()])

            # store the original number of winners
            # and the number of copies of the card we have
            copies[id] = [len(n.intersection(w)), 0]

    for i in range(1, max(copies.keys())):
        for j in range(copies[i][0]):
            num_copies = 1 + copies[i][1]
            next_card = i + j + 1
            copies[next_card][1] += num_copies

    # each card has 1 original and v[1] copies of it
    return sum(1 + value[1] for value in copies.values())


if __name__ == "__main__":
    print(part1())
    print(part2())
