from pathlib import Path
import numpy as np
import tomllib

def normalize(v):
    # Retorna un vector unitario manteniendo la dirección original.
    """Normaliza un vector."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    else:
        return v / norm

def ortho_proj_matrix(span, near, far) -> np.ndarray:
    # Construye matriz ortográfica centrada para escenas Z-up.
    depth = far - near
    row1 = np.array([1/span,      0,           0,         0], dtype=np.float32)
    row2 = np.array([0,            2/depth,     0,   (-2*near/depth)-1], dtype=np.float32)
    row3 = np.array([0,            0,     1/span,         0], dtype=np.float32)
    row4 = np.array([0,            0,           0,       1.0], dtype=np.float32)
    return np.vstack([row1, row2, row3, row4])


def perspective_proj_matrix(fov_y, near, far) -> np.ndarray:
    # Calcula proyección en perspectiva respetando el sistema Z-up.
    """
    Crea una matriz de proyección en perspectiva (Z-up, right-handed).
    """
    fov_lines_length = far/np.cos(fov_y / 2.0)
    far_span = fov_lines_length*np.sin(fov_y / 2.0)
    near_span = (far_span/far)*near


    row1 = np.array([far/far_span,0,0,0], dtype=np.float32)
    row2 = np.array([0,2/(far-near),0,-near/(far-near)], dtype=np.float32)
    row3 = np.array([0,0,far/far_span,0], dtype=np.float32)
    row4 = np.array([0,1,0,0], dtype=np.float32)
    return np.vstack([row1, row2, row3, row4]).astype(np.float32)

def to_tuple(value, fallback):
    # Convierte listas/tuplas a tuple y aplica fallback si es None.
    if value is None:
        return tuple(fallback)
    if isinstance(value, (list, tuple)):
        return tuple(value)
    return tuple(fallback)

def load_config(path: Path) -> dict:
    # Lee archivos TOML defensivamente devolviendo dict vacío si no existe.
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)

