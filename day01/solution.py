def part1() -> int:
    s = 0
    with open("puzzle", "r") as f:
        for line in f:
            document = line.strip()
            first_digit = None
            second_digit = None
            for i in range(0, len(document)):
                try:
                    first_digit = int(document[i])
                    break
                except ValueError:
                    continue

            for i in range(len(document) - 1, -1, -1):
                try:
                    second_digit = int(document[i])
                    break
                except ValueError:
                    continue
            calibration = f"{first_digit}{second_digit}"
            s += int(calibration)

    return s


n = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part2() -> int:
    s = 0
    with open("puzzle", "r") as f:
        for line in f:
            document = line.strip()
            for i in range(0, len(document)):
                first_digit = None
                try:
                    first_digit = int(document[i])
                    break
                except ValueError:
                    pass
                for j in range(3, 6):
                    if document[i : i + j] in n:
                        first_digit = n[document[i : i + j]]
                        break
                if first_digit is not None:
                    break
            for i in range(len(document) - 1, -1, -1):
                second_digit = None
                try:
                    second_digit = int(document[i])
                    break
                except ValueError:
                    pass
                if i <= len(document) - 3:
                    for j in range(3, 6):
                        if document[i : i + j] in n:
                            second_digit = n[document[i : i + j]]
                            break
                    if second_digit is not None:
                        break
            calibration = f"{first_digit}{second_digit}"
            s += int(calibration)
    return s


if __name__ == "__main__":
    # print(part1())
    print(part2())
