import requests
import base64
import random
import time
import os

from dotenv import load_dotenv
from deep_translator import GoogleTranslator

import streamlit as st

st.set_page_config(page_title="prompt to image GenAI", page_icon="🤖", layout="wide")
st.title("Generador de Imágenes con IA by Julián Dev")


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

spanish_prompt = st.chat_input("Escribe tu descripción para generar la imagen:")

if spanish_prompt:
    st.write(f"El usuario ha enviado el siguiente prompt: {spanish_prompt}")

    with st.spinner("generando imágenes...", show_time=True):
        time.sleep(3)

    images = []
    for i in range(3):
        st.write(f"Generando imagen {i + 1}...")
        english_prompt = translate_prompt(spanish_prompt)
        combined_prompt = f"{english_prompt}"

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

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print(f"La imagen {i + 1} fue generada exitosamente.")
            images.append(response.content)

            st.image(response.content, caption=f"Imagen generada con IA {i + 1}")

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"generated_image_{timestamp}_{i + 1}.jpg"

            with open(filename, "wb") as file:
                file.write(response.content)

            print(f"Imagen {i + 1} guardada como '{filename}'")
        else:
            print(f"Error en la solicitud: {response.status_code}, {response.text}")

    st.success("Generación de imágenes completada!")
