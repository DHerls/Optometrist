from .common import Exam, Question

from PIL import Image

def create_dummy_exam() -> Exam:
    image = Image.new('RGB', (128, 128), (255, 255, 255))
    prompt = "Is this image white? Respond only with 'YES' or 'NO'."
    answer = "YES"
    return Exam("dummy", [Question("dummy", prompt, image, answer)])
