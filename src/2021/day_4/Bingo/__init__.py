import re


class BingoPosition:
    value: int
    marked: bool

    def __init__(self, value: int):
        self.value = value
        self.marked = False

    def __str__(self):
        return "%d -> %s" % (self.value, self.marked)

    def __repr__(self):
        return self.__str__()


class BingoBoard:
    grid: [[BingoPosition]]

    def __init__(self, grid: [[BingoPosition]]):
        if len(grid) != 5:
            raise Exception("Invalid line count!")
        for line in grid:
            if len(line) != 5:
                raise Exception("Line \"%s\" does not contain 5 numbers!" % line)
        self.grid = grid

    def get_sum_of_unmarked_numbers(self) -> int:
        sum_of_board: int = 0
        for array in self.grid:
            for pos in array:
                if not pos.marked:
                    sum_of_board += pos.value
        return sum_of_board

    def mark_value(self, value: int):
        for array in self.grid:
            for pos in array:
                if pos.value == value:
                    pos.marked = True

    def has_board_won(self) -> bool:
        for y in range(len(self.grid)):
            counter_x: int = 0
            counter_y: int = 0
            for x in range(len((self.grid[y]))):
                if self.grid[x][y].marked:
                    counter_x += 1
                if self.grid[y][x].marked:
                    counter_y += 1
            if counter_x == 5 or counter_y == 5:
                return True
        return False

    def remove_all_marked_positions(self):
        for array in self.grid:
            for pos in array:
                pos.marked = False

    def __str__(self):
        value: str = ""
        for line in self.grid:
            value = "%s%s\n" % (value, line)
        return value

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def parse_bingo_field_lines_from_path(path: str) -> [str]:
        lines: [str] = []
        line_regex: str = r"\d+ +\d+ +\d+ +\d+ +\d+"
        for line in open(path):
            line = line.replace("\n", "")
            iterator = re.finditer(line_regex, line)
            for match in iterator:
                lines.append(match.group())
        if len(lines) % 5 != 0:
            raise Exception("Invalid line count \"%d\"" % len(lines))
        return lines


def parser_numbers_from_bingo_lines(lines: [str]) -> [BingoPosition]:
    result: [[BingoPosition]] = []
    for line in lines:
        next_line: [BingoPosition] = []
        iterator = re.finditer(r"\d+", line)
        for match in iterator:
            next_line.append(BingoPosition(int(match.group())))
        if len(next_line) != 5:
            raise Exception("Invalid number count in line \"%s\"" % line)
        result.append(next_line)
    return result


def parse_bingo_boards(path: str) -> [BingoBoard]:
    lines: [[BingoPosition]] = parser_numbers_from_bingo_lines(BingoBoard.parse_bingo_field_lines_from_path(path))
    boards: [BingoBoard] = []
    next_line: [[int]] = []
    for i, line in enumerate(lines):
        next_line.append(line)
        if (i + 1) % 5 == 0:
            boards.append(BingoBoard(next_line))
            next_line = []
    return boards


def parse_draw_numbers_from_path(path: str) -> [int]:
    results: [int] = []
    regex: str = r"(\d+(?=,)|(?<=,)\d)"
    for line in open(path):
        iterator = re.finditer(regex, line)
        for match in iterator:
            results.append(int(match.group()))
    return results


class BingoGame:
    draw_numbers: [int]
    bingo_boards: [BingoBoard]
    last_call: int = None
    last_counter: int = None
    wining_board_id: int

    def __init__(self, path: str):
        self.wining_board_id = 0
        self.last_counter = 0
        self.bingo_boards = parse_bingo_boards(path)
        self.draw_numbers = parse_draw_numbers_from_path(path)

    def get_last_winning_game(self) -> BingoBoard:
        self.remove_marker_from_all_boards()
        bingo_board_copy: [BingoBoard] = []

        for board in self.bingo_boards:
            bingo_board_copy.append(board)

        for number in self.draw_numbers:
            self.draw_number(number)
            boards_to_remove: [BingoBoard] = []
            for board in bingo_board_copy:
                if board.has_board_won() and len(bingo_board_copy) > 1:
                    boards_to_remove.append(board)
            for board in boards_to_remove:
                bingo_board_copy.remove(board)
            if len(bingo_board_copy) == 1 and bingo_board_copy[0].has_board_won():
                self.last_counter = number
                return bingo_board_copy[0]

        return None

    def play_game_until_winner(self) -> [{int, BingoBoard}]:
        self.remove_marker_from_all_boards()
        for number in self.draw_numbers:
            self.draw_number(number)
            possible_winners: [{int, BingoBoard}] = self.get_winning_boards()
            if len(possible_winners) > 0:
                self.last_call = number
                return possible_winners
        return []

    def remove_marker_from_all_boards(self):
        for board in self.bingo_boards:
            board.remove_all_marked_positions()

    def get_winning_boards(self) -> [{int, BingoBoard}]:
        winning_boards: [[int, BingoBoard]] = []
        for i, board in enumerate(self.bingo_boards):
            if board.has_board_won():
                winning_boards.append({
                    "position": i,
                    "board": board
                })
        return winning_boards

    def draw_number(self, value: int):
        for board in self.bingo_boards:
            board.mark_value(value)
