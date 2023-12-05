import re

def parse_row(row):
    id_raw, rest_raw = row.split("Card ")[1].split(": ")
    wining_raw, my_raw = rest_raw.split(" | ")
    id = int(id_raw.strip())
    wining = re.split("\s{1,}", wining_raw.strip())
    my = re.split("\s{1,}", my_raw.strip())
    score = 0
    matched = 0
    for one in wining:
        if one not in my:
            continue
        if score == 0:
            score = 1
        else:
            score *= 2
        matched += 1
    return { "id": id, "wining": wining, "my": my, "score": score, "matched": matched }

class Processor():
    def __init__(self, filepath):
        f = open(filepath, "r")
        csv_content = f.read()
        self.rows = csv_content.split("\n")

    

    def process(self):
        score_total = 0
        for row_raw in self.rows:
            row = parse_row(row_raw)
            print(row["score"])
            score_total += row["score"]
        return score_total

    def process2(self):
        cards = {}
        last_card_total = len(self.rows) + 1
        for row_raw in self.rows:
            # print(row_raw)
            print("CARDS: ")
            print(cards)
            row = parse_row(row_raw)
            print(row)
            if row["score"] == 0:
                continue
            last_card = min(last_card_total, row["id"] + row["matched"])
            for card in range(row["id"], last_card + 1):
                card_key = str(card)
                multiplier = 1 if card_key not in cards else cards[card_key]
                # print("Adding")
                query = {}
                if card_key in cards:
                    query = { card_key: cards[card_key] + multiplier }
                    # cards[card_key] = cards[card_key] + multiplier
                    print("(update " + card_key)
                else:
                    query = { card_key: multiplier }
                    # cards[card_key] = multiplier
                    print("(new " + card_key)
                print(query)
                cards.update(query)
                print("[" + card_key + "] mul: " + str(multiplier) + ", count: " + str(cards[card_key]))
        return cards


if __name__ == '__main__':
    filename = "../data/04.test.csv"
    # filename = "../data/04.csv"
    p = Processor(filename)
    print("1st")
    total = p.process()
    print("Total")
    print(str(total))

    print("2nd")
    cards = p.process2()
    print(cards)

