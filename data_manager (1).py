import json
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
