import re
import json
# map: [dest_from, source_from, length]

class Processor():
    def __init__(self, filepath):
        f = open(filepath, "r")
        csv_content = f.read()
        rows_raw = csv_content.split("\n")

        seeds_str = None
        for row in rows_raw:
            if seeds_str is not None:
                break
            seed_match = re.search("seeds:", row)
            if seed_match is None:
                continue
            seed_numbers_match = re.findall("[0-9]+", row)
            if len(seed_numbers_match) == 0:
                continue
            seeds_str = seed_numbers_match
            break

        order = []
        seeds = []
        for seed_str in seeds_str:
            seeds.append(int(seed_str))
        
        current_map = None
        seed_skipped = False
        maps = {}
        for row in rows_raw:
            print(row)
            if seed_skipped is False:
                seed_match = re.search("seeds:", row)
                if seed_match is not None:
                    seed_skipped = True
                    continue

            seed_map_match = re.findall("([a-z\s-]+)\s+map:", row)
            if len(seed_map_match) == 1:
                current_map = seed_map_match[0]
                order.append(current_map)
                maps[current_map] = []
                continue

            seed_map_numbers_match = re.findall("[0-9]+", row)
            if len(seed_map_numbers_match) > 0:
                map_numbers = []
                for nb in seed_map_numbers_match:
                    map_numbers.append(int(nb))
                maps[current_map].append(map_numbers)
        
        self.seeds = seeds
        self.maps = maps
        self.order = order
        print(seeds)
        print(maps)
        print(order)

    def process1st(self):
        print("\n===================\n\n\n")
        locations = []
        location_seq = []
        for seed in self.seeds:
            print("\n===================\nSeed: " + str(seed) + "\n----------------")
            value = seed
            dest = None
            location_seq.append(value)
            for map in self.order:
                print("\nMap [" + map + "]\n------------------------")
                print(self.maps[map])
                print("Source: " + str(value))
                for recipe in self.maps[map]:
                    [dest, source, length] = recipe
                    if value < source or value > (source + length):
                        continue
                    print("Recipe: " + json.dumps(recipe))
                    score = dest + (value - source)
                    print("Dest:   " + str(score))
                    value = score
                    location_seq.append(value)
                    break
            locations.append(value)

                
        print(locations)
        # print('seq:')
        # print(location_seq)
        return locations


            


if __name__ == '__main__':
    filename = "../data/05.txt"
    # filename = "../data/05.test.txt"
    # filename = "../data/05.test2.txt"
    p = Processor(filename)

    print("1st")
    result = p.process1st()
    print("Result")
    first = min(result)
    print(str(first))

