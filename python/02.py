class Processor():
    def __init__(self, filepath):
        f = open(filepath, "r")
        csv_content = f.read()
        self.rows = csv_content.split("\n")

    def split_row(self, row):
        id_raw, games_raw = row.split("Game ")[1].split(": ")
        id = int(id_raw)
        games = games_raw.split("; ")
        rgbs = []
        for game in games:
            rgb = self.game_to_rgb(game)
            rgbs.append(rgb)
        return (id, rgbs)


    def game_to_rgb(self, game):
        colors = [0, 0, 0]
        colors_raw = game.split(", ")
        for color_raw in colors_raw:
            nb_raw, color = color_raw.split(" ")
            nb = int(nb_raw)
            if color == 'red':
                colors[0] = nb
            elif color == 'green':
                colors[1] = nb
            elif color == 'blue':
                colors[2] = nb
        return colors

    def process(self, my_rgb):
        total = 0
        for row in self.rows:
            is_allowed = True
            (id, rgbs) = self.split_row(row)
            for rgb in rgbs:
                if rgb[0] > my_rgb[0] or rgb[1] > my_rgb[1] or rgb[2] > my_rgb[2]:
                    is_allowed = False
                    break
            if is_allowed is False:
                continue
            total += id
        return total
        
    def process_2nd(self):
        total = 0
        row_index = -1
        for row in self.rows:
            row_index += 1
            (_, rgbs) = self.split_row(row)
            rgb_max = [0, 0, 0]
            for rgb in rgbs:
                for index in range(0,3):
                    rgb_max[index] = max(rgb[index], rgb_max[index])
            row_sum = rgb_max[0]
            for index in range(1,3):
                row_sum *= rgb_max[index]
            print("Row " + str(row_index))
            print("Row sum " + str(row_sum))
            total += row_sum
        return total



if __name__ == '__main__':
    filename = "../data/02.test.csv"
    # filename = "../data/02.csv"
    p = Processor(filename)
    print("1st")
    total = p.process([12, 13, 14])
    print("Total")
    print(str(total))

    print("2nd")
    total = p.process_2nd()
    print("Total")
    print(str(total))
