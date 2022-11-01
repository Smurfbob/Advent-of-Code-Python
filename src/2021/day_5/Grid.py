from Line import Line
from Position import Position


class LineGrid:
    maze: [[int]]
    lines: [Line]

    def __init__(self, lines: [Line]):
        self.lines = lines
        self.maze = LineGrid.gen_maze_from_lines(self.lines)
        self.mark_positions()

    def mark_positions(self):







    @staticmethod
    def gen_maze_from_lines(lines: [Line]) -> [[int]]:
        result: [[int]] = []
        x_length: int = max(list(map(lambda l: l.start.x if l.start.x > l.end.x else l.end.x, lines))) + 1
        y_length: int = max(list(map(lambda l: l.start.y if l.start.y > l.end.y else l.end.y, lines))) + 1
        for x in range(x_length):
            next_row: [int] = []
            for y in range(y_length):
                next_row.append(0)
            result.append(next_row)
        return result
