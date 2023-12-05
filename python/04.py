import re

def get_wining(wining, my):
    score = 0
    matched = []
    for one in wining:
        # print(one)
        if one not in my:
            continue
        if score == 0:
            score = 1
        else:
            score *= 2
        matched.append(one)
    return [matched, score]
    
def parse_row(row):
    id_raw, rest_raw = row.split("Card ")[1].split(": ")
    wining_raw, my_raw = rest_raw.split(" | ")
    id = int(id_raw.strip())
    wining = re.split("\s{1,}", wining_raw.strip())
    my = re.split("\s{1,}", my_raw.strip())
    matched, score = get_wining(wining, my)
    return { "id": id, "wining": wining, "my": my, "score": score, "matched": matched }

class Processor():
    def __init__(self, filepath):
        f = open(filepath, "r")
        csv_content = f.read()
        rows_raw = csv_content.split("\n")
        self.rows = []
        for row_raw in rows_raw:
            row = parse_row(row_raw)
            self.rows.append(row)

    def process1st(self):
        score_total = 0
        for row in self.rows:
            score_total += row["score"]
        return score_total

    def process2nd(self):
        cards = {}
        last_card_total = len(self.rows) + 1
        for row in self.rows:
            id = row["id"]
            id_key = str(id)
            if id_key not in cards:
                cards[id_key] = 0
            cards[id_key] += 1
            if row["score"] == 0:
                continue
            last_card = min(last_card_total, row["id"] + len(row["matched"]))
            multiplier = cards[id_key]
            for card in range(row["id"] + 1, last_card + 1):
                card_key = str(card)
                query = {}
                if card_key in cards:
                    query = { card_key: cards[card_key] + multiplier }
                else:
                    query = { card_key: multiplier }
                cards.update(query)
        return cards

if __name__ == '__main__':
    # filename = "../data/04.test.csv"
    filename = "../data/04.csv"
    p = Processor(filename)

    print("1st")
    total = p.process1st()
    print("Total")
    print(str(total))

    print("2nd")
    cards = p.process2nd()
    total_cards = 0
    for value in cards.values():
        total_cards += value
    print("Total")
    print(str(total_cards))

