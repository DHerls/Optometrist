from src.models.openai_vision import OpenAiGptVision
from src.config import OPENAI_API_KEY
from PIL import Image

model = OpenAiGptVision(OPENAI_API_KEY)

img = Image.open(r"C:\Users\dan\Downloads\grid_with_red_square.png")

answer = model.ask_question("Which square of this image is colored red? Use the grid coordinates provided.", img)
print(answer)
