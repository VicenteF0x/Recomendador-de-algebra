import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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
