from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import requests
import google.generativeai as genai

class CrosswalkDetection(BaseModel):
    has_crosswalk: bool
    latitude: float | None = None
    longitude: float | None = None

def analyze_image(image_data, API_KEY) -> CrosswalkDetection:
    """
    Analiza una imagen (and its metadata) para detectar la presencia de un paso peatonal
    y devuelve la información de detección junto con las coordenadas.
    """
    genai.configure(api_key=API_KEY)

    try:
        image_url = image_data['url']
        latitude = image_data['lat']
        longitude = image_data['lng']

        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image_content = BytesIO(response.content)
        img = Image.open(image_content)

        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"Hay un paso peatonal para personas en esta imagen? Responde 'true' o 'false'."
        gemini_response = model.generate_content([img, prompt])

        has_crosswalk = False
        if gemini_response.text and "true" in gemini_response.text.lower():
            has_crosswalk = True

        return CrosswalkDetection(has_crosswalk=has_crosswalk, latitude=latitude, longitude=longitude)

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")
        return CrosswalkDetection(has_crosswalk=False)
    except Exception as e:
        print(f"Error al analizar la imagen: {e}")
        return CrosswalkDetection(has_crosswalk=False)