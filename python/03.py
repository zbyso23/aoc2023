import re

class Grid():
    def __init__(self, width, height):
        rows, cols = (height, width)
        self.data = [[None]*rows]*cols
        self.symbols_checked = False

    def get_id(self, x, y):
        return (x + 1) + ((y + 1) * (len(self.data[0]) + 1))

    def parse_row(self, y, row_raw):
        row = [*row_raw]
        digits = []
        for index in range(0, len(row)):
            value = row[index]
            res = re.search("[0-9]", value)
            if res is not None:
                if len(digits) == 0:
                    row[index] = { "type": "digit", "value": value, "start_index": index, "digit_part": False, "length": 1, "total": None, "is_symbol_around": False, "id": str(self.get_id(index, y)) }
                else:
                    row[index] = { "type": "digit", "value": value, "start_index": index - len(digits), "digit_part": True }
                digits.append(value)
                if index < len(row) - 1:
                    continue
                
            if value == '.':
                row[index] = { "type": "empty", "value": None }
            elif res is None:
                row[index] = { "type": "symbol", "value": value }

            if len(digits) == 0:
                continue

            last_digit = row[index - 1]
            nb_raw = "".join(digits)
            nb = int(nb_raw)
            is_symbol_around = False if value == '.' else True
            row[last_digit["start_index"]]["length"] = len(digits)
            row[last_digit["start_index"]]["total"] = nb
            row[last_digit["start_index"]]["is_symbol_around"] = is_symbol_around
            digits = []
        self.data[y] = row
        self.symbols_checked = False
        print("ROW " + str(y + 1))
        for col in row:
            print(col)


    def _check_symbol(self, x, y, value):
        y_min = max(0, y - 1)
        y_max = min(len(self.data), y + 2)
        x_min = max(0, x - 1)
        x_max = min(len(self.data[0]), x + 2)
        for row in range(y_min, y_max):
            for col in range(x_min, x_max):
                if (row == y and col == x) or self.data[row][col]["type"] != "digit":
                    continue

                if self.data[row][col]["type"] == "digit":
                    digit_index = self.data[row][col]["start_index"]
                    self.data[row][digit_index]["is_symbol_around"] = True
                    print("...NUMBER: " + self.data[row][digit_index]["total"])


    def check_symbols(self):
        for row in range(0, len(self.data)):
            for col in range(0, len(self.data[0])):
                cell = self.data[row][col]
                if cell["type"] != "symbol":
                    continue
                print("Checking Symbol [" + cell["value"] + "]")
                self._check_symbol(col, row, cell["value"])


    def get(self):
        if self.symbols_checked == False:
            self.check_symbols()
        return self.data

    



class Processor():
    def __init__(self, filepath):
        f = open(filepath, "r")
        csv_content = f.read()
        self.rows = csv_content.split("\n")
        rows = len(self.rows)
        cols = len(self.rows[0])
        for row in self.rows:
            cols = max(len(row), cols)
        self.grid = Grid(cols, rows)

    def print(self):
        data = self.grid.get()
        for row_index in range(0, len(data)):
            row = []
            for cell in data[row_index]:
                row.append(cell["value"] if cell["value"] is not None else " ")
            print("".join(row))

    def process(self):
        row_index = 0
        for row in self.rows:
            self.grid.parse_row(row_index, row)
            row_index += 1

        already_added = []
        total_diff = 0
        total = 0
        data = self.grid.get()
        for row in data:
            for cell in row:
                if cell["type"] != "digit" or cell["digit_part"] == True or cell["is_symbol_around"] == False:
                    continue
                # print("NB ID " + cell["id"])
                total_diff += cell["total"]
                if cell["id"] in already_added:
                    continue
                already_added.append(cell["id"])
                total += cell["total"]
        print("Total Diff: " + str(total_diff))
        return total




if __name__ == '__main__':
    filename = "../data/03.test2.csv"
    # filename = "../data/03.csv"
    p = Processor(filename)
    print("1st")
    total = p.process()
    print("Total")
    print(str(total))

