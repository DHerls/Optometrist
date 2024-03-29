import argparse

from src.config import GOOGLE_API_KEY, OPENAI_API_KEY
from src.models.common import VisionModel
from src.exams.common import Exam
from src.models.openai_vision import OpenAiGptVision
from src.models.google_gemini import GoogleGemini
from src.exams.dummy import create_dummy_exam
from src.exams.alignment_chart_single import create_alignment_chart_single_fill_exam
from src.exams.battleship_single import create_battleship_single_fill_exam
from src.exams.lrc_single_fill import create_lrc_single_fill_exam
from src.exams.lrc_multi_fill import create_lrc_multi_fill_exam
from src.results import save_run

import logging

"""
If the following line doesn't exist, and Google Gemini is the only model used in a Windows environment, you will get `AttributeError: module 'PIL' has no attribute 'PngImagePlugin'`

See: https://stackoverflow.com/a/69125762
"""
from PIL import PngImagePlugin

log = logging.getLogger("run_exams")

MODELS = {
    "openai":  OpenAiGptVision(OPENAI_API_KEY),
    "google": GoogleGemini(GOOGLE_API_KEY)
}

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def evaluate(models: list[VisionModel], exams: list[Exam]):
    all_results = []
    for exam in exams:
        for model in models:
            total_questions = len(exam.questions)
            log.info("Starting to evaluate %s for %s: %s questions", exam.name, model.name, total_questions)
            results = exam.evaluate(model)
            num_correct = len(list(filter(lambda r: r.matches, results)))
            log.info("Finished evaluating %s for %s: %s/%s correct", exam.name, model.name, num_correct, total_questions)
            all_results.extend(results)
    save_run(all_results)


def dummy(model_names: list[str], **kwargs):
    exam = create_dummy_exam()
    evaluate(get_models(model_names), [exam])


def lrc_single_fill(model_names: list[str], cell_sizes: list[int], **kwargs):
    exams = [create_lrc_single_fill_exam(size) for size in cell_sizes]
    evaluate(get_models(model_names), exams)


def lrc_multi_fill(model_names: list[str], cell_sizes: list[int], **kwargs):
    exams = [create_lrc_multi_fill_exam(size) for size in cell_sizes]
    evaluate(get_models(model_names), exams)


def alignment_chart_single_fill(model_names: list[str], cell_sizes: list[int], **kwargs):
    exams = [create_alignment_chart_single_fill_exam(size) for size in cell_sizes]
    evaluate(get_models(model_names), exams)


def battleship_single_fill(model_names: list[str], cell_sizes: list[int], grid_sizes: list[int], **kwargs):
    exams = [create_battleship_single_fill_exam(cell_size, grid_size) for cell_size in cell_sizes for grid_size in grid_sizes]
    evaluate(get_models(model_names), exams)


def get_models(model_names: list[str]) -> list[VisionModel]:
    return [MODELS.get(n) for n in list(set(model_names))]


def main():
    parser = argparse.ArgumentParser(
        prog='Vision Model Special Reasoning Exam Suite',
        description='Evaluate the effectiveness of vision models at spatial reasoning problems'
    )

    parser.add_argument("--model", dest="model_names", action="append", help="Specify which models to run exams against.", choices=sorted(list(MODELS.keys())))

    subparsers = parser.add_subparsers(required=True)

    dummy_parser = subparsers.add_parser("dummy", help="Send a single question to each model to validate connectivity")
    dummy_parser.set_defaults(func=dummy)

    lrc_single_fill_parser = subparsers.add_parser("lrc_single_fill", help="Left-Right-Center questions, one square is filled in")
    lrc_single_fill_parser.add_argument("--cell-size", dest='cell_sizes', type=int, action='append', help="Specify cell size of generated images. Include more than once to test multiple sizes. Default is 10, 50 and 150.")
    lrc_single_fill_parser.set_defaults(func=lrc_single_fill)

    lrc_multi_fill_parser = subparsers.add_parser("lrc_multi_fill", help="Left-Right-Center questions, all squares is filled in")
    lrc_multi_fill_parser.add_argument("--cell-size", dest='cell_sizes', type=int, action='append', help="Specify cell size of generated images. Include more than once to test multiple sizes. Default is 10, 50 and 150.")
    lrc_multi_fill_parser.set_defaults(func=lrc_multi_fill)

    alignment_chart_single_fill_parser = subparsers.add_parser("alignment_chart_single_fill", help="A 3x3 grid of squares with no coordinate system. One cell filled in.")
    alignment_chart_single_fill_parser.add_argument("--cell-size", dest='cell_sizes', type=int, action='append', help="Specify cell size of generated images. Include more than once to test multiple sizes. Default is 10, 50 and 150.")
    alignment_chart_single_fill_parser.set_defaults(func=alignment_chart_single_fill)

    battleship_single_fill_parser = subparsers.add_parser("battleship_single_fill", help="A variable-sized grid of squares with an alphanumeric coordinate system. One cell filled in.")
    battleship_single_fill_parser.add_argument("--cell-size", dest='cell_sizes', type=int, action='append', help="Specify cell size of generated images. Include more than once to test multiple sizes. Default is 10, 50 and 150.")
    battleship_single_fill_parser.add_argument("--grid-size", dest='grid_sizes', type=int, action='append', help="Specify grid size. Include more than once to test multiple sizes. Default is 4, 6 and 9.")
    battleship_single_fill_parser.set_defaults(func=battleship_single_fill)

    args = parser.parse_args()

    if 'model_names' in args and args.model_names is None:
        args.model_names = ['openai', 'google']
    
    if 'cell_sizes' in args and args.cell_sizes is None:
        args.cell_sizes = [10, 50, 150]
    
    if 'grid_sizes' in args and args.grid_sizes is None:
        args.grid_sizes = [4, 6, 9]

    args.func(**vars(args))


if __name__ == "__main__":
    main()
