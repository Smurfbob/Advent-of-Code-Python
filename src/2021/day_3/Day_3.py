class NumberArray:
    lines: [str]

    @staticmethod
    def gen_line_array_from_path(path: str) -> [str]:
        lines: [str] = []
        for line in open(path):
            lines.append(line.replace("\n", ""))
        return lines

    def __init__(self, path: str):
        self.lines = self.gen_line_array_from_path(path)

    def get_column(self, column: int) -> [int]:
        result: [int] = []
        for line in self.lines:
            result.append(int(line[column]))
        return result

    def get_all_columns(self) -> [[int]]:
        columns: [[int]] = []
        for i in range(len(self.lines[0])):
            columns.append(self.get_column(i))
        return columns


def resolve_gamma_rate(num_array: NumberArray) -> str:
    gam: str = ""
    for column in num_array.get_all_columns():
        gam = "%s%d" % (gam, 1 if column.count(1) > column.count(0) else 0)
    return gam


def revers_binary(binary: str) -> str:
    return binary.replace("0", "3").replace("1", "0").replace("3", "1")


# Returns -1 when both have the same frequency
def find_most_common_bit(lines: [str], position: int) -> int:
    bits: [int] = list(map(lambda el: int(el[position]), lines))
    return 1 if bits.count(1) > bits.count(0) else 0 if bits.count(0) > bits.count(1) else -1


# Returns -1 when both have the same frequency
def find_least_common_bit(lines: [str], position: int) -> int:
    bits: [int] = list(map(lambda el: int(el[position]), lines))
    return 1 if bits.count(1) < bits.count(0) else 0 if bits.count(0) < bits.count(1) else -1


def resolve_rating(numer_array: NumberArray, bit_resolver, keeper) -> str:
    lines: [str] = numer_array.lines.copy()
    position: int = 0
    while len(lines) > 1:
        frequent_bit: int = bit_resolver(lines, position)
        frequent_bit = keeper(frequent_bit)
        to_remove: [str] = []
        for line in lines:
            if not line[position] == "%d" % frequent_bit:
                to_remove.append(line)
        for line_to_remove in to_remove:
            lines.remove(line_to_remove)
        position = position + 1 if position + 1 < len(lines[0]) else 0
    return lines[0]


number_array = NumberArray("resource/input.txt")
gamma: str = resolve_gamma_rate(number_array)
epsilon: str = revers_binary(gamma)
power_consumption: int = int(gamma, 2) * int(epsilon, 2)
keep_value = lambda value_to_keep: lambda el: el if el != -1 else value_to_keep
oxygen_rating: str = resolve_rating(number_array, find_most_common_bit, keep_value(1))
co_two_scrubber_rating: str = resolve_rating(number_array, find_least_common_bit, keep_value(0))

print("Part one")
print("Gamma: %s decimal %d" % (gamma, int(gamma, 2)))
print("Epsilon: %s decimal %d" % (epsilon, int(epsilon, 2)))
print("Power consumption: %d\n" % power_consumption)
print("Part two")
print("Oxygen: %s decimal %d" % (oxygen_rating, int(oxygen_rating, 2)))
print("CO2: %s decimal %d" % (co_two_scrubber_rating, int(co_two_scrubber_rating, 2)))
print("Life support: %d" % (int(oxygen_rating, 2) * int(co_two_scrubber_rating, 2)))
