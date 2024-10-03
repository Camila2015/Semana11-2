import os
import streamlit as st
import base64
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Configuración inicial de la página
st.set_page_config(layout="wide")
st.title("Momento Art-Attack - Detección de dibujos")

# Barra lateral para personalizar la línea
st.sidebar.header("Personalización de la línea")
stroke_color = st.sidebar.color_picker("Selecciona el color de la línea", '#FFFFFF')
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
bg_color = st.sidebar.color_picker("Selecciona el color de fondo", '#000000')

# Seleccionar el tipo de línea para dibujar
drawing_mode = st.sidebar.selectbox(
    "Selecciona el tipo de dibujo",
    ("freedraw", "line", "rect", "circle", "point")
)

# Crear el componente de lienzo
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno con opacidad
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=500,
    width=800,
    drawing_mode=drawing_mode,
    key="canvas"
)

# Función para codificar imagen en base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# Input para clave API de OpenAI
ke = st.text_input('Ingresa tu Clave API de OpenAI')
os.environ['OPENAI_API_KEY'] = ke

# Verificar si se ingresó la API key
api_key = os.environ['OPENAI_API_KEY']

# Botón para analizar la imagen dibujada
analyze_button = st.button("Analiza la imagen")

# Verificar que hay imagen, API key y que se presionó el botón de analizar
if canvas_result.image_data is not None and api_key and analyze_button:

    with st.spinner("Analizando ..."):
        # Convertir la imagen del canvas a formato PIL
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')

        # Codificar la imagen en base64
        base64_image = encode_image_to_base64("img.png")

        # Texto del prompt para la IA
        prompt_text = "Describe en español brevemente lo que se ve en la imagen"

        # Preparar el payload para la solicitud de completado
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",  # Cambia por el modelo que prefieras
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt_text}\n![image](data:image/png;base64,{base64_image})"
                    }
                ],
                max_tokens=500,
            )
            full_response = response.choices[0].message['content']
            st.write("Descripción del dibujo:")
            st.markdown(full_response)
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
else:
    if not api_key:
        st.warning("Por favor ingresa tu API key.")
