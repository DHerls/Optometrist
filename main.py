from src.generators.grid import GridOptions, create_grid, fill_grid_cell

from src.exams.lrc_single_fill import create_question, Positions
from src.exams.common import Colors


question = create_question(Positions.CENTER, Colors.GREEN)

print(question.prompt)
print(question.answer)
question.image.save("question.png")
