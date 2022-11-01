from Line import read_lines_from_input_path
from Line import Line
from Grid import LineGrid

lines: [Line] = read_lines_from_input_path("resource/testInput.txt")
grid: LineGrid = LineGrid(lines)
for lul_und_lal in grid.maze:
    print(lul_und_lal)
