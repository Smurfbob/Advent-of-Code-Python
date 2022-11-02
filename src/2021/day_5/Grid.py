from Line import Line
from Position import Position


class LineGrid:
    maze: [[int]]
    lines: [Line]

    def __init__(self, lines: [Line]):
        self.lines = lines
        self.maze = LineGrid.gen_maze_from_lines(self.lines)
        self.mark_positions()

    @staticmethod
    def add_if_not_present(array: [Position], position: Position):
        present: bool = False
        for pos in array:
            if pos.__eq__(position):
                present = True
        if not present:
            array.append(position)

    @staticmethod
    def gen_position_set_from_lines(lines: [Line]) -> [Position]:
        positions: [Position] = []
        for line in lines:
            for pos in line.positions:
                LineGrid.add_if_not_present(positions, pos)
        return positions

    @staticmethod
    def count_positions_in_array(array: [Position], pos: Position):
        counter: int = 0
        for position in array:
            if position.__eq__(pos):
                counter += 1
        return counter

    def gen_position_count_array(self) -> [{int, Position}]:
        position_set: [Position] = LineGrid.gen_position_set_from_lines(self.lines)
        position_count_array: [{int, Position}] = []
        for pos in position_set:
            counter: int = 0
            for line in self.lines:
                counter += LineGrid.count_positions_in_array(line.positions, pos)
            position_count_array.append({
                "count": counter,
                "position": pos
            })
        return position_count_array

    @staticmethod
    def filter(condition, array: [any]) -> [any]:
        results: [any] = []
        for value in array:
            if condition(value):
                results.append(value)
        return results

    def mark_positions(self):
        positions_greate_one: [{int, Position}] = LineGrid.filter(lambda el: el["count"] > 1,
                                                                  self.gen_position_count_array())
        for value in positions_greate_one:
            number: int = value["count"]
            position: Position = value["position"]
            self.maze[position.x][position.y] = number

    @staticmethod
    def gen_maze_from_lines(lines: [Line]) -> [[int]]:
        result: [[int]] = []
        x_length: int = 10  # max(list(map(lambda l: l.start.x if l.start.x > l.end.x else l.end.x, lines))) + 1
        y_length: int = 10  # max(list(map(lambda l: l.start.y if l.start.y > l.end.y else l.end.y, lines))) + 1
        for x in range(x_length):
            next_row: [int] = []
            for y in range(y_length):
                next_row.append(0)
            result.append(next_row)
        return result
