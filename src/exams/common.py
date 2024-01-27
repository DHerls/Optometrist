from PIL.Image import Image

from dataclasses import dataclass

@dataclass
class Color:
    name: str
    value: tuple[int, int, int]


class Question:

    def __init__(self, prompt: str, image: Image, answer: str) -> None:
        self.prompt = prompt
        self.image = image
        self.answer = answer


@dataclass
class Colors:
    BLACK = Color("black", (0, 0, 0))
    WHITE = Color("white", (255, 255, 255))
    RED = Color("red", (255, 0, 0))
    GREEN = Color("green", (0, 255, 0))
    BLUE = Color("blue", (0, 0, 255))
