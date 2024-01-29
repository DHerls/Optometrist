from PIL.Image import Image

from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

from ..models.common import VisionModel

log = logging.getLogger("exams.common")

@dataclass
class Color:
    name: str
    value: tuple[int, int, int]


class Question:
    name: str
    prompt: str
    image: Image
    answer: str

    def __init__(self, name: str, prompt: str, image: Image, answer: str) -> None:
        self.name = name
        self.prompt = prompt
        self.image = image
        self.answer = answer
    
    def evaluate_response(self, model_answer: str) -> bool:
        processed_response = model_answer.replace(' ', '').replace('.', '').lower()
        return self.answer.lower() == processed_response


@dataclass
class XPosition:
    name: str
    value: int


class XPositions:
    LEFT = XPosition("LEFT", 0)
    CENTER = XPosition("CENTER", 1)
    RIGHT = XPosition("RIGHT", 2)

@dataclass
class YPosition:
    name: str
    value: int


class YPositions:
    TOP = YPosition("TOP", 0)
    MIDDLE = YPosition("MIDDLE", 1)
    BOTTOM = YPosition("BOTTOM", 2)


class Colors:
    BLACK = Color("BLACK", (0, 0, 0))
    WHITE = Color("WHITE", (255, 255, 255))
    RED = Color("RED", (255, 0, 0))
    GREEN = Color("GREEN", (0, 255, 0))
    BLUE = Color("BLUE", (0, 0, 255))
    CYAN = Color("CYAN", (0, 255, 255))
    YELLOW = Color("YELLOW", (255, 255, 0))
    MAGENTA = Color("MAGENTA", (255, 0, 255))
    GREY = Color("GREY", (120, 120, 120))


@dataclass
class Result:
    model_name: str
    exam_name: str
    question: Question
    model_response: str
    matches: bool
    ran_at: datetime
    duration: timedelta


class Exam:

    def __init__(self, name: str, questions: list[Question]) -> None:
        self.name = name
        self.questions = questions
    
    def evaluate(self, model: VisionModel) -> list[Result]:
        results = []
        for i, q in enumerate(self.questions):
            log.info("Asking question %s - %s", i, q.name)
            start = datetime.now()
            response = model.ask_question(q.prompt, q.image)
            duration = datetime.now() - start
            answer_matches = q.evaluate_response(response)
            log.info("Response: %s, Matches: %s", response, answer_matches)
            results.append(Result(model.name, self.name, q, response, answer_matches, start, duration))
        return results
