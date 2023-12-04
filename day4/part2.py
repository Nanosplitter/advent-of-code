def read_input():
    with open("input.txt") as f:
        return f.readlines()

lines = read_input()

class Card:
    def __init__(self, id, nums, wins):
        self.id = id
        self.nums = nums
        self.wins = wins
    
    def get_num_winning_nums(self):
        return len(list(filter(lambda x: x in self.wins, self.nums)))
    
    def __str__(self):
        return f"{self.id}: {self.nums} | {self.wins}"
    
    def __repr__(self):
        return f"{self.id}: {self.nums} | {self.wins}"

def process_cards(cards):
    if len(cards) == 0:
        return 0
    
    total = 0
    for i in range(len(cards)):
        num_cards_gotten = cards[i].get_num_winning_nums()
        total += process_cards(cards[i + 1:num_cards_gotten + 1]) + 1
    return total + len(cards)

cards = []

for line in lines:
    parts = line.split(":")
    card_parts = parts[1].split("|")

    nums = card_parts[0].split()
    wins = card_parts[1].split()

    cards.append(Card(parts[0], nums, wins))

print(process_cards(cards))
    