from .common import Question, Color
from ..generators.grid import create_grid, fill_grid_cell, GridOptions

from dataclasses import dataclass

@dataclass
class Position:
    name: str
    value: int


@dataclass
class Positions:
    LEFT = Position("LEFT", 0)
    CENTER = Position("CENTER", 1)
    RIGHT = Position("RIGHT", 2)


PROMPT = """You are being shown a grid with three squares. Which one of the squares is filled in? Respond with one of LEFT, CENTER, or RIGHT."""


def create_question(position: Position, fill: Color) -> Question:

    grid_options = GridOptions((50, 50), (3, 1))
    grid = create_grid(grid_options)

    fill_grid_cell(grid_options, grid, (position.value, 0), fill.value, 0)

    return Question(PROMPT, grid, position.name)
