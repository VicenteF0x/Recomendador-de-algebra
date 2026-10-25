import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from core.data_manager import cargar_json, guardar_json
from app.visualizations import plot_radar

st.title("👥 Gestión de Vectores (Usuarios y Películas)")
usuarios = cargar_json("usuarios.json")
peliculas = cargar_json("peliculas.json")
generos = ["Acción", "Romance", "Comedia", "Ciencia Ficción"]

col1, col2 = st.columns(2)
with col1:
    st.subheader("Añadir / Editar Usuario")
    nombre_u = st.text_input("Nombre del usuario")
    v_u = [st.slider(f"{g} (Usuario)", 0, 5, 0, key=f"u_{g}") for g in generos]
    if st.button("Guardar Usuario"):
        if nombre_u:
            usuarios[nombre_u] = v_u
            guardar_json("usuarios.json", usuarios)
            st.success("¡Guardado!")

with col2:
    st.subheader("Añadir / Editar Película")
    nombre_p = st.text_input("Nombre de la película")
    v_p = [st.slider(f"{g} (Peli)", 0, 5, 0, key=f"p_{g}") for g in generos]
    if st.button("Guardar Película"):
        if nombre_p:
            peliculas[nombre_p] = v_p
            guardar_json("peliculas.json", peliculas)
            st.success("¡Guardado!")

st.divider()
st.subheader("Explorador Visual de $R^4$")
seleccion_u = st.multiselect("Ver perfiles de usuarios", list(usuarios.keys()), default=list(usuarios.keys())[:2])
if seleccion_u:
    vectores_plot = {u: usuarios[u] for u in seleccion_u}
    st.plotly_chart(plot_radar(vectores_plot, generos), width="stretch")
