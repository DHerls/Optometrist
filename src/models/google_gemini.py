from PIL.Image import Image
from .common import VisionModel

import google.generativeai as genai

class GoogleGemini(VisionModel):

    name = "gemini-pro-vision"

    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')
    
    def ask_question(self, prompt: str, image: Image) -> str:
        response = self.model.generate_content([prompt, image], stream=True)
        response.resolve()
        return response.text.strip()
