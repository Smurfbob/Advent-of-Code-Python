CONST_VALUE: str = "value"
CONST_TYPE: str = "type"
CONST_NO_MEASUREMENT: str = "N/A - no previous measurement"
CONST_INCREASED: str = "increased"
CONST_DECREASED: str = "decreased"


def is_valid_index(index: int, bound: int) -> bool:
    return 0 <= index < bound


def read_path_to_integer_array(path: str) -> [int]:
    lines = []
    file = open(path)
    for line_value in file:
        lines.append(int(line_value))
    return lines


def map_array_by_using_two_values(arr: [any], first_value_consumer, two_value_mapper) -> [any]:
    if len(arr) == 0:
        return []
    result: [any] = [first_value_consumer(arr[0])]
    index_now = 0
    index_next = index_now + 1
    while is_valid_index(index_now, len(arr)) and is_valid_index(index_next, len(arr)):
        now = arr[index_now]
        nex = arr[index_next]
        result.append(two_value_mapper(nex, now))
        index_now += 1
        index_next = index_now + 1
    return result


def gen_measurement_array(array: [int]) -> [{}]:
    return map_array_by_using_two_values(array,
                                         lambda first_value: {CONST_VALUE: first_value,
                                                              CONST_TYPE: CONST_NO_MEASUREMENT},
                                         lambda a, b: {CONST_VALUE: a,
                                                       CONST_TYPE: CONST_INCREASED if a > b else CONST_DECREASED})


def count_measurements(array: [int]) -> int:
    measurements: [{}] = gen_measurement_array(array)
    return list(map(lambda measurement: measurement[CONST_TYPE], measurements)).count(CONST_INCREASED)


def map_array_by_using_three_values(arr: [any], three_value_mapper) -> [int]:
    if len(arr) == 0:
        return []
    result: [int] = []
    first = 0
    second = first + 1
    third = second + 1
    while is_valid_index(first, len(arr)) and is_valid_index(second, len(arr)) and is_valid_index(third, len(arr)):
        result.append(three_value_mapper(arr[first], arr[second], arr[third]))
        first += 1
        second = first + 1
        third = second + 1
    return result


print("Part one answer: %d " % count_measurements(read_path_to_integer_array("resource/input_1.txt")))

print("Part two answer: %d" % count_measurements(
    map_array_by_using_three_values(read_path_to_integer_array("resource/input_1.txt"), lambda a, b, c: a + b + c)))
