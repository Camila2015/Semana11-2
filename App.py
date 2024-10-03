import os
import streamlit as st
import base64
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Función para codificar la imagen en base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# Configuración de la página
st.set_page_config(page_title='Tablero Inteligente', layout="wide")
st.title('Tablero Inteligente')

# Sidebar para ingresar API key
with st.sidebar:
    st.subheader("Acerca de:")
    st.subheader("En esta aplicación veremos la capacidad que ahora tiene una máquina de interpretar un boceto.")
    ke = st.text_input('Ingresa tu Clave de API de OpenAI', type='password')

# Seleccionar opciones para el canvas
st.sidebar.header("Personalización de la línea")
stroke_color = st.sidebar.color_picker("Selecciona el color de la línea", '#000000')
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
bg_color = st.sidebar.color_picker("Selecciona el color de fondo", '#FFFFFF')

drawing_mode = st.sidebar.selectbox(
    "Selecciona el tipo de dibujo",
    ("freedraw", "line", "rect", "circle", "point")
)

# Crear el canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=500,
    width=800,
    drawing_mode=drawing_mode,
    key="canvas"
)

# Verificar si hay una imagen en el canvas
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
    input_numpy_array = np.array(canvas_result.image_data)
    input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
    input_image.save('img.png')

# Analizar la imagen cuando se presiona el botón
analyze_button = st.button("Analiza la imagen")

if analyze_button and ke:
    os.environ['OPENAI_API_KEY'] = ke  # Guardar la API key en las variables de entorno
    api_key = os.environ['OPENAI_API_KEY']

    # Verificar si se tiene la API key
    if api_key and canvas_result.image_data is not None:
        st.write("Analizando la imagen...")
        with st.spinner("Procesando..."):
            try:
                # Codificar la imagen en base64
                base64_image = encode_image_to_base64("img.png")

                prompt_text = "Describe in Spanish briefly the image"
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # Cambia esto por el modelo que estés usando
                    messages=[
                        {"role": "user", "content": prompt_text},
                        {
                            "role": "user",
                            "content": {
                                "type": "image_url",
                                "image_url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                    max_tokens=500,
                )

                # Mostrar la respuesta
                st.write(response.choices[0].message['content'])

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor, sube una imagen y asegúrate de que tu API key es correcta.")
else:
    st.info("Ingresa tu API key y dibuja algo en el panel para empezar.")


