import streamlit as st
import sys
import os

# Asegurar que Streamlit encuentre la carpeta core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.data_manager import inicializar_datos_demo

st.set_page_config(page_title="Álgebra Lineal & Recomendaciones", page_icon="🎬", layout="wide")
inicializar_datos_demo()

st.title("🎬 Motor de Recomendaciones con Álgebra Lineal")
st.markdown(r'''
¡Bienvenido! Esta aplicación semiprofesional demuestra cómo el **Álgebra Lineal** es el motor detrás de sistemas de recomendación modernos, algoritmos de ciberseguridad y análisis de datos.

### Conceptos Matemáticos Demostrados:
*   **Vectores en $R^n$:** Cada usuario y película es un punto en un espacio de 4 dimensiones.
*   **Producto Punto ($a \cdot b$):** Mide cuánto de un vector "va en la dirección" del otro.
*   **Norma Euclídea ($||v||$):** La longitud del vector desde el origen.
*   **Similitud Coseno:** El coseno del ángulo entre dos vectores.
*   **Combinaciones Lineales ($c_1v_1 + c_2v_2$):** Usadas para fusionar perfiles.

Usa el menú lateral para explorar cada módulo.
''')
