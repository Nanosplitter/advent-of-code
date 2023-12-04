def read_input():
    with open("input.txt") as f:
        return f.readlines()

cards = read_input()

total = 0

for card in cards:
    parts = card.split(":")
    card_parts = parts[1].split("|")

    nums = card_parts[0].split()
    wins = card_parts[1].split()

    num_winning_nums = len(list(filter(lambda x: x in wins, nums)))

    points = int(2 ** (num_winning_nums - 1))

    total += points
    #print(num_winning_nums)
print(total)
    