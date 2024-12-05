def read_input():
    with open("input.txt") as f:
        return f.readlines()

lines = read_input()

class Card:
    def __init__(self, id, nums, wins):
        self.id = id - 1
        self.nums = nums
        self.wins = wins
    
    def get_num_winning_nums(self):
        return len(list(filter(lambda x: x in self.wins, self.nums)))

cards = []

for line in lines:
    parts = line.split(":")
    id = parts[0].split()[1]
    card_parts = parts[1].split("|")

    nums = card_parts[0].split()
    wins = card_parts[1].split()

    cards.append(Card(int(id), nums, wins))

ending_cards = [1] * len(cards)

for card in cards:
    for i in range(card.id + 1, card.id + card.get_num_winning_nums() + 1):
        ending_cards[i] += ending_cards[card.id]

print(sum(ending_cards))