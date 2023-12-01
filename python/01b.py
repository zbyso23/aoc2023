import re


class RowProcessor():
    def __init__(self):
        self.digits_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        digits = []
        for nb in range(1,10):
            digits.append(str(nb))
        self.digits = digits
        self.numbers_re = "(" + "|".join(self.digits_words) + "|" + "|".join(self.digits) + ")"
        
    def process_digit(self, digit):
        if re.match("[a-z]{1,}", digit):
            return (self.digits_words.index(digit) + 1)
        return int(digit)
    
    def find_in_row(self, row):
        parts = []
        row_copy = row[:]
        is_runing = True
        while is_runing:
            x = re.search(self.numbers_re, row_copy)
            if x is None:
                break
            parts.append(x.group())
            row_copy = row_copy[x.start() + 1:]
            if len(row_copy) == 0:
                break
        return parts

        
    
    def process_row(self, row):
        print(row)
        numbers = self.find_in_row(row)
        print(numbers)
        if len(numbers) == 0:
            return None
        
        first = self.process_digit(numbers[0])
        last = self.process_digit(numbers[len(numbers) - 1])
        return [first, last]
    
    def debug_row(self, row):
        m = re.finditer(self.numbers_re, row)
        parts = []
        for x in m:
            row[x.start():x.end()]
            parts.append(x)
        print(parts)
        


class Processor():
    def __init__(self, filepath):
        f = open(filepath, "r")
        csv_content = f.read()
        self.rows = csv_content.split("\n")
        self.rp = RowProcessor()

    def process(self):
        total = 0
        for row in self.rows:
            res = self.rp.process_row(row)
            if res is None:
                continue

            first, last = res
            nb = int(str(first) + str(last))
            print((first, last))
            total += nb
        return total


filename = "../data/01.csv"
p = Processor(filename)
total = p.process()


print("total")
print(total)