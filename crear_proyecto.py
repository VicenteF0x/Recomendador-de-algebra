import os
import subprocess
import sys

# ==========================================
# 1. DEFINICION DE LA ESTRUCTURA Y CODIGO
# ==========================================

# Cabecera que se pone en cada pagina para que encuentre las carpetas core/ y app/
CABECERA_PAGINA = """import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
"""

archivos = {
    "requirements.txt": """streamlit>=1.50.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.18.0
pytest>=7.0.0
""",

    "core/__init__.py": "",

    "core/algebra.py": """import numpy as np
from typing import List, Dict, Any


def producto_punto(v1: np.ndarray, v2: np.ndarray) -> float:
    return float(np.dot(v1, v2))


def norma(v: np.ndarray) -> float:
    return float(np.linalg.norm(v))


def similitud_coseno(v1: np.ndarray, v2: np.ndarray) -> float:
    norma_v1 = norma(v1)
    norma_v2 = norma(v2)
    if norma_v1 == 0 or norma_v2 == 0:
        return 0.0
    return producto_punto(v1, v2) / (norma_v1 * norma_v2)


def angulo_vectores(v1: np.ndarray, v2: np.ndarray) -> float:
    similitud = similitud_coseno(v1, v2)
    similitud = max(-1.0, min(1.0, similitud))
    angulo_rad = np.arccos(similitud)
    return float(np.degrees(angulo_rad))


def combinacion_lineal(vectores: List[np.ndarray], pesos: List[float]) -> np.ndarray:
    if len(vectores) != len(pesos):
        raise ValueError("La cantidad de vectores y pesos debe ser igual.")
    resultado = np.zeros_like(vectores[0], dtype=float)
    for v, c in zip(vectores, pesos):
        resultado += c * v
    return resultado


def explicar_calculo_similitud(v1: np.ndarray, v2: np.ndarray, nombre1: str = "A", nombre2: str = "B") -> Dict[str, Any]:
    pp = producto_punto(v1, v2)
    n1 = norma(v1)
    n2 = norma(v2)
    sim = similitud_coseno(v1, v2)
    ang = angulo_vectores(v1, v2)
    desglose_pp = " + ".join([f"({x}*{y})" for x, y in zip(v1, v2)])
    return {
        "producto_punto": f"{nombre1}·{nombre2} = {desglose_pp} = {pp:.2f}",
        "normas": f"||{nombre1}|| = {n1:.2f}, ||{nombre2}|| = {n2:.2f}",
        "formula": f"cos(θ) = {pp:.2f} / ({n1:.2f} * {n2:.2f})",
        "resultado": f"Similitud: {sim:.4f}",
        "angulo": f"Ángulo: {ang:.1f}°"
    }
""",

    "core/data_manager.py": """import json
import os
from typing import Dict, Any

DATA_DIR = "data"


def asegurar_directorios():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def cargar_json(filename: str) -> Dict[str, Any]:
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def guardar_json(filename: str, data: Dict[str, Any]):
    asegurar_directorios()
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def inicializar_datos_demo():
    asegurar_directorios()
    usuarios_file = "usuarios.json"
    peliculas_file = "peliculas.json"

    usuarios_demo = {
        "Ana": [5, 1, 3, 4],
        "Beto": [4, 2, 3, 5],
        "Carla": [1, 5, 4, 1]
    }
    peliculas_demo = {
        "Misión Galáctica": [5, 0, 1, 5],
        "Amor en París": [0, 5, 2, 0],
        "Noche de Risas": [1, 3, 5, 0]
    }

    if not os.path.exists(os.path.join(DATA_DIR, usuarios_file)):
        guardar_json(usuarios_file, usuarios_demo)
    if not os.path.exists(os.path.join(DATA_DIR, peliculas_file)):
        guardar_json(peliculas_file, peliculas_demo)
""",

    "app/__init__.py": "",

    "app/visualizations.py": """import plotly.graph_objects as go
import numpy as np


def plot_radar(vectores_dict: dict, categorias: list) -> go.Figure:
    fig = go.Figure()
    for nombre, vector in vectores_dict.items():
        fig.add_trace(go.Scatterpolar(
            r=list(vector) + [vector[0]],
            theta=categorias + [categorias[0]],
            fill='toself',
            name=nombre
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=True, title="Perfil de Vectores en R^4")
    return fig


def plot_angulo_2d(norma_v1: float, norma_v2: float, angulo_grados: float, nombre1: str, nombre2: str) -> go.Figure:
    angulo_rad = np.radians(angulo_grados)
    x1, y1 = norma_v1, 0.0
    x2, y2 = norma_v2 * np.cos(angulo_rad), norma_v2 * np.sin(angulo_rad)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, x1], y=[0, y1], mode='lines+markers+text', name=nombre1, text=["", nombre1], textposition="bottom right", line=dict(width=4)))
    fig.add_trace(go.Scatter(x=[0, x2], y=[0, y2], mode='lines+markers+text', name=nombre2, text=["", nombre2], textposition="top right", line=dict(width=4)))
    max_val = max(norma_v1, norma_v2) * 1.2
    fig.update_layout(xaxis=dict(range=[-max_val/2, max_val]), yaxis=dict(range=[-max_val/2, max_val], scaleanchor="x", scaleratio=1), title=f"Proyección 2D del Ángulo: {angulo_grados:.1f}°", showlegend=True)
    return fig
""",

    # r""" para que \cdot no sea una secuencia de escape invalida
    "app/main.py": r"""import streamlit as st
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
""",

    "app/pages/1_Usuarios_y_Peliculas.py": CABECERA_PAGINA + """
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
""",

    "app/pages/2_Recomendaciones.py": CABECERA_PAGINA + """
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
        st.code(f"1) {pasos['producto_punto']}\\n2) {pasos['normas']}\\n3) {pasos['formula']}\\n4) {pasos['resultado']} ({pasos['angulo']})")

st.divider()
st.subheader("Usuarios con gustos similares (Ángulo Mínimo)")
otros_usuarios = {u: np.array(v) for u, v in usuarios.items() if u != usuario_actual}
if otros_usuarios:
    mas_similar = max(otros_usuarios.items(), key=lambda x: similitud_coseno(v_user, x[1]))
    nom_sim, v_sim = mas_similar
    ang = angulo_vectores(v_user, v_sim)
    st.success(f"**{nom_sim}** es el usuario más similar a {usuario_actual} (Ángulo: {ang:.1f}°)")
    st.plotly_chart(plot_angulo_2d(norma(v_user), norma(v_sim), ang, usuario_actual, nom_sim), width="stretch")
""",

    "app/pages/3_Perfil_Grupal.py": CABECERA_PAGINA + """
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
""",

    "app/pages/4_Ciberseguridad.py": CABECERA_PAGINA + """
import streamlit as st
import numpy as np
from core.algebra import similitud_coseno

st.title("🛡️ Ciberseguridad: Detección de Anomalías")
perfil_normal = np.array([5, 2, 10, 14])
cuentas = {
    "Empleado_1": np.array([6, 3, 12, 15]),
    "Empleado_2": np.array([4, 1, 8, 13]),
    "Hacker_Bot_99": np.array([100, 50, 200, 3]),
}

umbral = st.slider("Umbral de Similitud (coseno)", 0.0, 1.0, 0.8)
st.write(f"**Vector Normal Esperado:** `{list(perfil_normal)}`")

for nombre, vector in cuentas.items():
    sim = similitud_coseno(perfil_normal, vector)
    if sim < umbral:
        st.error(f"🚨 **{nombre}** | Similitud: {sim:.4f} - ¡COMPORTAMIENTO ANÓMALO!")
    else:
        st.success(f"✅ **{nombre}** | Similitud: {sim:.4f} - Normal")
""",

    "app/pages/5_MovieLens.py": CABECERA_PAGINA + """
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
"""
}

# ==========================================
# 2. CONSTRUCCION DEL PROYECTO
# ==========================================

print("Construyendo la arquitectura del proyecto...")

for carpeta in ["core", "app", "app/pages", "data", "tests"]:
    os.makedirs(carpeta, exist_ok=True)

for ruta, contenido in archivos.items():
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("Archivo creado:", ruta)

print("\nProyecto construido con exito.")

# ==========================================
# 3. EJECUCION AUTOMATICA
# ==========================================

if "--sin-ejecutar" in sys.argv:
    sys.exit(0)

print("Iniciando Streamlit (se abrira una pestana en tu navegador)...")

try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])
except Exception as e:
    print("\nError al iniciar Streamlit automaticamente:", e)
    print("Para iniciar manualmente, escribe en tu terminal:")
    print("python -m streamlit run app/main.py")
