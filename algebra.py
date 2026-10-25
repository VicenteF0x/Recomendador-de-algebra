import numpy as np
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
