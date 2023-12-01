import re

f = open("../data/01.csv", "r")
csv_content = f.read()
content = csv_content.split("\n")
total = 0
for row in content:
    numbers = re.findall("[0-9]{1,1}", row)
    if len(numbers) == 0:
        continue

    first = numbers[0]
    last = numbers[len(numbers) - 1]
    nb = int(first + last)
    total += nb
    print(nb)

print("total")
print(total)