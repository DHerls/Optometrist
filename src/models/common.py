from abc import ABC, abstractmethod
from PIL.Image import Image

from io import BytesIO
import base64

class VisionModel(ABC):

    @abstractmethod
    def ask_question(self, prompt: str, image: Image) -> str:
        pass


def image_to_png_b64(image: Image) -> str:
    png_bytes = BytesIO()
    image.save(png_bytes, format='PNG')
    return base64.b64encode(png_bytes.getvalue()).decode('utf-8')
