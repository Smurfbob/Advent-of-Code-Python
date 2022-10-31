import re

CONST_COMMAND_REGEX = r"^(forward|down|up) (\d+)$"


class Command:
    FORWARD: str = "forward"
    DOWN: str = "down"
    UP: str = "up"

    value: int
    direction: str

    def __init__(self, value: str, direction: str):
        if direction not in [self.FORWARD, self.DOWN, self.UP]:
            raise Exception("Value \"%s\" is not a valid direction" % direction)
        self.value = int(value)
        self.direction = direction

    def __str__(self):
        return "{value: %s, direction: %s}" % (self.value, self.direction)


def read_path_to_line_array(path: str) -> [str]:
    file = open(path)
    result: [str] = []
    for line in file:
        result.append(line.replace("\n", ""))
    return result


def map_line_to_command(line: str) -> Command:
    matcher = re.finditer(CONST_COMMAND_REGEX, line, re.MULTILINE)
    matches = []
    for match in matcher:
        matches.append(match)
    if len(matches) > 1 or len(matches) == 0:
        raise Exception("No match for line \"%s\"" % line)
    return Command(matches[0].group(2), matches[0].group(1))


def parse_commands_from_path(path: str) -> [Command]:
    return list(map(map_line_to_command, read_path_to_line_array(path)))


def calc_positions_from_commands_par_one(commands: [Command]) -> int:
    def filter_by_direction(direction: str) -> [Command]:
        return filter(lambda command: command.direction == direction, commands)

    horizontal: int = 0
    depth: int = 0
    for el in filter_by_direction(Command.FORWARD):
        horizontal += el.value
    for el in filter_by_direction(Command.DOWN):
        depth += el.value
    for el in filter_by_direction(Command.UP):
        depth -= el.value
    return horizontal * depth


def calc_positions_from_commands_par_two(commands: [Command]) -> int:
    horizontal: int = 0
    depth: int = 0
    aim: int = 0
    for command in commands:
        if command.direction == Command.FORWARD:
            horizontal += command.value
            depth += (aim * command.value)
        if command.direction == Command.DOWN:
            aim += command.value
        if command.direction == command.UP:
            aim -= command.value
    return horizontal * depth


coms: [Command] = parse_commands_from_path("resource/input.txt")
print("Part one: %d" % calc_positions_from_commands_par_one(coms))
print("Part two: %d" % calc_positions_from_commands_par_two(coms))
