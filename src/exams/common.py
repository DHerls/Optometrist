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


@dataclass
class Question:
    name: str
    prompt: str
    image: Image
    answer: str


class Colors:
    BLACK = Color("BLACK", (0, 0, 0))
    WHITE = Color("WHITE", (255, 255, 255))
    RED = Color("RED", (255, 0, 0))
    GREEN = Color("GREEN", (0, 255, 0))
    BLUE = Color("BLUE", (0, 0, 255))


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
            answer_matches = response == q.answer
            log.info("Response: %s, Matches: %s", response, answer_matches)
            results.append(Result(model.name, self.name, q, response, answer_matches, start, duration))
        return results
