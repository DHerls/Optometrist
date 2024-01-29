from .exams.common import Result

from datetime import datetime
from pathlib import Path
import csv

def save_run(results: list[Result]):
    current_directory = Path('.')
    
    current_time_str = datetime.now().strftime(r"%Y_%m_%d_%H_%M_%S_%f")

    run_directory_name = f"{current_time_str}"

    run_directory = current_directory.joinpath("exam_runs", run_directory_name)
    run_directory.mkdir(parents=True, exist_ok=False)

    run_images_directory = run_directory.joinpath("img")
    run_images_directory.mkdir(exist_ok=False)

    rows = []
    for i, result in enumerate(results):
        image_path = run_images_directory.joinpath(f"{i}_{result.question.name}.png")
        result.question.image.save(image_path, format='PNG')

        rows.append({
            "result_num": i,
            "model_name": result.model_name,
            "exam_name": result.exam_name,
            "question_name": result.question.name,
            "question_prompt": result.question.prompt,
            "question_image": str(image_path),
            "question_answer": result.question.answer,
            "result_model_response": result.model_response,
            "result_timestamp": result.ran_at.isoformat(),
            "result_duration_milli": int(result.duration.microseconds / 1000),
            "result_answer_matches": result.matches
        })
    
    csv_path = run_directory.joinpath(f"results_{current_time_str}.csv")
    
    with open(csv_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, ["result_num", "model_name", "exam_name", "question_name", "question_prompt", "question_image", "question_answer", "result_model_response", "result_timestamp", "result_duration_milli", "result_answer_matches"])
        writer.writeheader()
        writer.writerows(rows)
