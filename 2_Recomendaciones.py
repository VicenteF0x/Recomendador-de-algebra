import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import numpy as np
from core.data_manager import cargar_json
from core.algebra import similitud_coseno, angulo_vectores, explicar_calculo_similitud, norma
from app.visualizations import plot_angulo_2d

st.title("🎬 Recomendaciones y Similitud")
usuarios = cargar_json("usuarios.json")
peliculas = cargar_json("peliculas.json")

if not usuarios or not peliculas:
    st.warning("No hay datos.")
    st.stop()

usuario_actual = st.selectbox("Selecciona un usuario para recomendarle:", list(usuarios.keys()))
v_user = np.array(usuarios[usuario_actual])
st.write(f"Vector de **{usuario_actual}**: `{list(v_user)}`")
modo_explicacion = st.checkbox("🔍 Activar Modo Explicación (Álgebra Lineal)")

st.subheader("Top Películas Recomendadas")
recomendaciones = []
for peli, v_p in peliculas.items():
    sim = similitud_coseno(v_user, np.array(v_p))
    recomendaciones.append((peli, sim, np.array(v_p)))
recomendaciones.sort(key=lambda x: x[1], reverse=True)

for peli, sim, v_p in recomendaciones:
    st.metric(label=peli, value=f"Similitud: {sim:.4f}")
    if modo_explicacion:
        st.info("Cálculo matemático paso a paso:")
        pasos = explicar_calculo_similitud(v_user, v_p, usuario_actual, peli)
        st.code(f"1) {pasos['producto_punto']}\n2) {pasos['normas']}\n3) {pasos['formula']}\n4) {pasos['resultado']} ({pasos['angulo']})")

st.divider()
st.subheader("Usuarios con gustos similares (Ángulo Mínimo)")
otros_usuarios = {u: np.array(v) for u, v in usuarios.items() if u != usuario_actual}
if otros_usuarios:
    mas_similar = max(otros_usuarios.items(), key=lambda x: similitud_coseno(v_user, x[1]))
    nom_sim, v_sim = mas_similar
    ang = angulo_vectores(v_user, v_sim)
    st.success(f"**{nom_sim}** es el usuario más similar a {usuario_actual} (Ángulo: {ang:.1f}°)")
    st.plotly_chart(plot_angulo_2d(norma(v_user), norma(v_sim), ang, usuario_actual, nom_sim), width="stretch")
