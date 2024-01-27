from PIL.Image import Image
from .common import VisionModel, image_to_png_b64

import requests

class OpenAiGptVision(VisionModel):

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
    
    def ask_question(self, prompt: str, image: Image) -> str:
        image_b64 = image_to_png_b64(image)
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json=payload
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
