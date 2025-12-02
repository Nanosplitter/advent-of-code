def part1(rotations: list[(str, int)]) -> int:
    dial = 50

    count = 0

    for rotation in rotations:
        if rotation[0] == "R":
            dial += rotation[1]
        else:
            dial -= rotation[1]

        dial %= 100

        if dial == 0:
            count += 1

    return count


def part2(rotations: list[(str, int)]) -> int:
    dial = 50
    count = 0

    for rotation in rotations:
        start_pos = dial
        movement = rotation[1]

        full_rotations = movement // 100

        count += full_rotations

        movement %= 100

        if rotation[0] == "R":
            dial += movement
        else:
            dial -= movement

        if dial <= 0:
            count += 1 if not start_pos == 0 else 0
        if dial >= 100:
            count += 1

        dial %= 100

    return count


with open("./input.txt") as f:
    input = f.readlines()
    rotations = []

    for line in input:
        direction = line[0]
        amount = int(line[1:])

        rotations.append((direction, amount))

    print(part1(rotations))
    print(part2(rotations))
