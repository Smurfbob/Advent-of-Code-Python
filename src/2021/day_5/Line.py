from Position import Position
import re


class Line:
    start: Position
    end: Position
    positions: [Position]

    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.start = Position(x1, y1)
        self.end = Position(x2, y2)
        self.positions = []
        self.resolve_positions()

    def __str__(self):
        return "%d,%d -> %d,%d" % (self.start.x, self.start.y, self.end.x, self.end.y)

    def add_position_if_not_present(self, position: Position):
        present: bool = False
        for pos in self.positions:
            if Line.is_same_position(position, pos):
                present = True
        if not present:
            self.positions.append(Position(position.x, position.y))

    @staticmethod
    def is_same_position(a: Position, b: Position) -> bool:
        return a.x == b.x and a.y == b.y

    def resolve_x_positions(self, start: Position, end: Position):
        while start.x != end.x:
            if start.x < end.x:
                start.x += 1
            elif start.x > end.x:
                start.x -= 1
            self.add_position_if_not_present(start)

    def resolve_y_positions(self, start: Position, end: Position):
        while start.y != end.y:
            if start.y < end.y:
                start.y += 1
            elif start.y > end.y:
                start.y -= 1
            self.add_position_if_not_present(start)

    def resolve_positions(self):
        start_copy: Position = Position(self.start.x, self.start.y)
        end_copy: Position = Position(self.end.x, self.end.y)
        self.add_position_if_not_present(start_copy)
        if Line.is_same_position(start_copy, end_copy):
            return
        self.resolve_x_positions(start_copy, end_copy)
        if Line.is_same_position(start_copy, end_copy):
            return
        self.resolve_y_positions(start_copy, end_copy)


def read_lines_from_input_path(path: str) -> [Line]:
    lines: [Line] = []
    regex: str = r"^(\d+),(\d+) -> (\d+),(\d+)$"
    for line in open(path):
        found_match = False
        matcher = re.finditer(regex, line)
        for match in matcher:
            x1: int = int(match.group(1))
            y1: int = int(match.group(2))
            x2: int = int(match.group(3))
            y2: int = int(match.group(4))
            lines.append(Line(x1, y1, x2, y2))
            found_match = True
        if not found_match:
            raise Exception("No match found for line \"%s\"" % line)
    return lines


def print_lines(lines: [Line]):
    for line in lines:
        print(line)
        print(list(map(lambda el: el.__str__(), line.positions)))
