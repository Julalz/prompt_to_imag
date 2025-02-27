import requests
import base64
import random
import time
import os

from dotenv import load_dotenv
from deep_translator import GoogleTranslator


def image_file_to_base64(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode("utf-8")


def generate_random_seed():
    return random.randint(1, 99999)


def image_url_to_base64(image_url):
    response = requests.get(image_url)
    image_data = response.content
    return base64.b64encode(image_data).decode("utf-8")






def translate_prompt(prompt, src_lang="es", dest_lang="en"):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    translated = translator.translate(prompt)
    print(f"Traducción: {translated}")
    return translated





load_dotenv()
api_key = os.getenv("api_key_segmind")

url = "https://api.segmind.com/v1/ideogram-txt-2-img"


spanish_prompt = (
    "dame un un gato egipcion de color negro encima de una moto custom"
)
spanish_prompt2 = "el fondo debe de estar estilo carretera con un bosque"


english_prompt = translate_prompt(spanish_prompt)
english_prompt2 = translate_prompt(spanish_prompt2)
combined_prompt = f"{english_prompt} + {english_prompt2}"


random_seed = generate_random_seed()

data = {
    "magic_prompt_option": "AUTO",
    "negative_prompt": "low quality, blurry, no weird proportions, no weird anatomy, low resolution, distorted",
    "prompt": combined_prompt,
    "resolution": "RESOLUTION_1024_1024",
    "seed": random_seed,
    "style_type": "REALISTIC",
}

headers = {"x-api-key": api_key}

response =  requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("La imagen fue generada exitosamente.")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"generated_image_{timestamp}.jpg"

    with open(filename, "wb") as file:
        file.write(response.content)

    print(f"Imagen guardada como '{filename}'")
else:
    print(f"Error en la solicitud: {response.status_code}, {response.text}")
