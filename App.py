import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.title("Tablero")


st.sidebar.header("Personalización de la línea")


stroke_color = st.sidebar.color_picker("Selecciona el color de la línea", '#FFFFFF')


stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 15)


bg_color = st.sidebar.color_picker("Selecciona el color de fondo", '#000000')


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
