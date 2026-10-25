import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import numpy as np
from core.data_manager import cargar_json
from core.algebra import combinacion_lineal, similitud_coseno

st.title("🤝 Perfil Grupal (Combinación Lineal)")
usuarios = cargar_json("usuarios.json")
peliculas = cargar_json("peliculas.json")

seleccion = st.multiselect("Selecciona los usuarios del grupo:", list(usuarios.keys()))
if seleccion:
    pesos = []
    vectores = []
    cols = st.columns(len(seleccion))
    for i, u in enumerate(seleccion):
        with cols[i]:
            w = st.slider(f"Peso de {u}", 0.0, 1.0, 1.0 / len(seleccion), key=f"w_{u}")
            pesos.append(w)
            vectores.append(np.array(usuarios[u]))

    v_grupo = combinacion_lineal(vectores, pesos)
    st.info(f"**Vector Resultante:** `[{', '.join([f'{x:.2f}' for x in v_grupo])}]`")

    st.subheader("Mejor película para el grupo:")
    mejor_peli, max_sim = None, -1
    for peli, v_p in peliculas.items():
        sim = similitud_coseno(v_grupo, np.array(v_p))
        if sim > max_sim:
            max_sim, mejor_peli = sim, peli
    st.success(f"🍿 **{mejor_peli}** (Similitud: {max_sim:.4f})")
