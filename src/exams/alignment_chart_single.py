from .common import Question, Color, Colors, Exam, XPosition, XPositions, YPosition, YPositions
from ..generators.grid import create_grid, fill_grid_cell, GridOptions


PROMPT = """You are being shown 3x3 grid of squares. Which one of the squares is filled in? Respond in the format X,Y where X is one of LEFT, RIGHT, or CENTER and Y is one of TOP, MIDDLE, or BOTTOM"""


def create_question(x_position: XPosition, y_position: YPosition, fill: Color, cell_size: int) -> Question:

    grid_options = GridOptions((cell_size, cell_size), (3, 3))
    grid = create_grid(grid_options)

    fill_grid_cell(grid_options, grid, (x_position.value, y_position.value), fill.value, 0)

    return Question(f"{x_position.name} {y_position.name} {fill.name}", PROMPT, grid, f"{x_position.name},{y_position.name}")


def create_alignment_chart_single_fill_exam(cell_size: int) -> Exam:

    questions = [
        create_question(x, y, Colors.RED, 50)
        for x in [XPositions.LEFT, XPositions.CENTER, XPositions.RIGHT]
        for y in [YPositions.TOP, YPositions.MIDDLE, YPositions.BOTTOM]
    ]
    return Exam(f"alignment_chart_single_fill_{cell_size}", questions)
