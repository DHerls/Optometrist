from .common import Question, Color, Colors, Exam, Position, Positions
from ..generators.grid import create_grid, fill_grid_cell, GridOptions


PROMPT = """You are being shown a grid with three squares. Which one of the squares is filled in? Respond with one of LEFT, CENTER, or RIGHT."""


def create_question(position: Position, fill: Color, cell_size: int) -> Question:

    grid_options = GridOptions((cell_size, cell_size), (3, 1))
    grid = create_grid(grid_options)

    fill_grid_cell(grid_options, grid, (position.value, 0), fill.value, 0)

    return Question(f"{position.name} {fill.name}", PROMPT, grid, position.name)


def create_lrc_single_fill_exam(cell_size: int) -> Exam:

    questions = [
        create_question(p, f, cell_size) for p in [Positions.LEFT, Positions.CENTER, Positions.RIGHT] for f in [Colors.BLACK, Colors.RED, Colors.GREEN, Colors.BLUE]
    ]
    return Exam(f"lrc_single_fill_{cell_size}", questions)
