from .common import Question, Color, Colors, Exam, XPosition, XPositions
from ..generators.grid import create_grid, fill_grid_cell, GridOptions

import random

from PIL.Image import Image


PROMPT = """You are being shown a grid with three squares. Which one of the squares is filled in with the color {}? Respond with one of LEFT, CENTER, or RIGHT."""


def create_question(squares: tuple[Color, Color, Color], winner: XPosition, cell_size: int) -> Image:

    grid_options = GridOptions((cell_size, cell_size), (3, 1))
    grid = create_grid(grid_options)

    names = []
    for i in range(3):
        fill_grid_cell(grid_options, grid, (i, 0), squares[i].value, 0)
        names.append(squares[i].name)
    
    name = ' '.join(names) + " - " + winner.name

    return Question(name, PROMPT.format(squares[winner.value].name), grid, winner.name)


def create_lrc_multi_fill_exam(cell_size: int) -> Exam:
    questions = [
        create_question((Colors.GREEN, Colors.BLUE, Colors.RED), XPositions.LEFT, cell_size),
        create_question((Colors.GREEN, Colors.BLUE, Colors.RED), XPositions.CENTER, cell_size),
        create_question((Colors.GREEN, Colors.BLUE, Colors.RED), XPositions.RIGHT, cell_size),
        create_question((Colors.CYAN, Colors.YELLOW, Colors.MAGENTA), XPositions.LEFT, cell_size),
        create_question((Colors.CYAN, Colors.YELLOW, Colors.MAGENTA), XPositions.CENTER, cell_size),
        create_question((Colors.CYAN, Colors.YELLOW, Colors.MAGENTA), XPositions.RIGHT, cell_size),
        create_question((Colors.BLACK, Colors.GREY, Colors.WHITE), XPositions.LEFT, cell_size),
        create_question((Colors.BLACK, Colors.GREY, Colors.WHITE), XPositions.CENTER, cell_size),
        create_question((Colors.BLACK, Colors.GREY, Colors.WHITE), XPositions.RIGHT, cell_size),
    ]

    return Exam(f"lrc_multi_fill_{cell_size}", questions)
