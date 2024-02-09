from .common import Question, Color, Colors, Exam
from ..generators.grid import create_grid, fill_grid_cell, GridOptions, XYPair

import string


PROMPT = """You are being shown a grid of squares. Which one of the squares is filled in? Respond with only the coordinate of the filled in square. An example answer would be A7."""


def create_question(cell_size: int, grid_size: int, fill: Color, position: XYPair) -> Question:

    grid_options = GridOptions((cell_size, cell_size), (grid_size, grid_size), line_width=3, coords_type="alphanum")
    grid = create_grid(grid_options)

    fill_grid_cell(grid_options, grid, position, fill.value, 0)

    answer_x = string.ascii_uppercase[position[0]]
    answer_y = string.digits[position[1] + 1]

    return Question(f"{grid_size}x{grid_size} {answer_x}{answer_y} {fill.name}", PROMPT, grid, f"{answer_x}{answer_y}")


def create_battleship_single_fill_exam(cell_size: int, grid_size: int) -> Exam:

    questions = [
        create_question(cell_size, grid_size, Colors.RED, (x, y))
        for x in range(grid_size)
        for y in range(grid_size)
    ]
    return Exam(f"battleship_{grid_size}x{grid_size}_{cell_size}", questions)
