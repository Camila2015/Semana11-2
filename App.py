import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title("Tablero")

# Barra lateral para personalizar la línea
st.sidebar.header("Personalización de la línea")

# Seleccionar color de la línea
stroke_color = st.sidebar.color_picker("Selecciona el color de la línea", '#FFFFFF')

# Seleccionar ancho de la línea
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 15)

# Establecer color de fondo
bg_color = st.sidebar.color_picker("Selecciona el color de fondo", '#000000')

# Crear componente de lienzo
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno fijo con algo de opacidad
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=400,
    width=400,
    key="canvas",
    drawing_mode="freedraw"
)
