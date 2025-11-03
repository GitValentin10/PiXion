from pathlib import Path
import numpy as np
import yaml

def normalize(v):
    """Normaliza un vector."""
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def ortho_proj_matrix(aspect_ratio, span, near, far) -> np.ndarray:
    abs_x = span * aspect_ratio
    abs_z = span
    depth = far - near


    row1 = np.array([1/abs_x,      0,           0,         0], dtype=np.float32)
    row2 = np.array([0,            2/depth,     0,   -near-1], dtype=np.float32)
    row3 = np.array([0,            0,     1/abs_z,         0], dtype=np.float32)
    row4 = np.array([0,            0,           0,       1.0], dtype=np.float32)
    return np.vstack([row1, row2, row3, row4])


def to_tuple(value, fallback):
    if value is None:
        return tuple(fallback)
    if isinstance(value, (list, tuple)):
        return tuple(value)
    return tuple(fallback)

def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}
