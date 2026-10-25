import plotly.graph_objects as go
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
