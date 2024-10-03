import openai
import os
import base64
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Configuración de la página
st.set_page_config(layout="wide")  
st.title("Momento Art-Attack")

# Barra lateral para personalizar la línea
st.sidebar.header("Personalización de la línea")

# Seleccionar color de la línea
stroke_color = st.sidebar.color_picker("Selecciona el color de la línea", '#FFFFFF')

# Seleccionar ancho de la línea
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)

# Seleccionar color de fondo
bg_color = st.sidebar.color_picker("Selecciona el color de fondo", '#000000')

# Seleccionar el tipo de línea para dibujar
drawing_mode = st.sidebar.selectbox(
    "Selecciona el tipo de dibujo",
    ("freedraw", "line", "rect", "circle", "point")
)

# Crear el componente de lienzo
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno con opacidad
    stroke_width=stroke_width,  # Ancho de la línea
    stroke_color=stroke_color,  # Color de la línea
    background_color=bg_color,  # Color de fondo
    height=500,
    width=800,
    drawing_mode=drawing_mode,  # Tipo de dibujo (línea, círculo, etc.)
    key="canvas"
)

# API Key de OpenAI
ke = st.text_input('Ingresa tu Clave API de OpenAI', type="password")
openai.api_key = ke

# Botón para analizar la imagen
analyze_button = st.button("Analiza la imagen")

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# Procesar la imagen y llamar a OpenAI cuando se hace clic en el botón
if canvas_result.image_data is not None and analyze_button:

    # Convertir el dibujo en una imagen y guardarla
    input_numpy_array = np.array(canvas_result.image_data)
    input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
    input_image.save('img.png')

    # Codificar la imagen en base64
    base64_image = encode_image_to_base64("img.png")
    
    prompt_text = "Describe the image."

    try:
        # Hacer la solicitud a la API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",  # O el modelo que prefieras
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )
        
        # Mostrar la respuesta en Streamlit
        st.write(response['choices'][0]['message']['content'])
    
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")


