import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import pandas as pd
from core.algebra import similitud_coseno

st.title("📊 Dataset Real: MovieLens")
st.caption("Usa el ratings.csv de ml-latest-small (el dataset completo es demasiado grande).")
archivo = st.file_uploader("Sube ratings.csv de MovieLens", type=['csv'])

if archivo is not None:
    df = pd.read_csv(archivo)
    st.write("Muestra de datos:", df.head(3))

    if st.button("Calcular similitud entre los primeros 2 usuarios"):
        matriz = df.pivot(index='userId', columns='movieId', values='rating').fillna(0)
        u1, u2 = matriz.iloc[0].values, matriz.iloc[1].values
        sim = similitud_coseno(u1, u2)
        st.info(f"Dimensión del espacio (cantidad de películas): $R^{{{len(u1)}}}$")
        st.success(f"Similitud Coseno entre Usuario 1 y 2: **{sim:.4f}**")
