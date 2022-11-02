import re


class BingoField:
    field: [[int]]

    def __init__(self, fie: [[int]]):
        if len(fie) != 5:
            raise Exception("Invalid line count %d" % len(fie))
        for line in fie:
            if len(line) != 5:
                raise Exception("Line \"%s\" has not 5 entries" % len(line))
        self.field = fie


class BingoContainer:
    bingo_fields: [BingoField]
    numbers: [int]

    def __init__(self, path: str):
        next_array: [int] = []
        self.bingo_fields = []
        for i, line in enumerate(open(path)):
            line = line.replace("\n", "")
            if i == 0:
                self.numbers = list(map(lambda el: int(el), line.split(",")))
            elif line != "":
                number_array: [int] = []
                matcher = re.finditer("\\d+", line)
                for match in matcher:
                    value = match.group(0)
                    number_array.append(int(value))
                next_array.append(number_array)
            if len(next_array) == 5:
                self.bingo_fields.append(BingoField(next_array))
                next_array = []


bingo_container = BingoContainer("resource/test_input.txt")

for field in bingo_container.bingo_fields:
    print(field)
