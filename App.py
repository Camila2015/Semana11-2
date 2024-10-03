import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")  # Ajusta el layout a 'wide' para mayor espacio
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

# Mostrar el resultado en el canvas
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)

