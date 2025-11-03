import numpy as np
from dataclasses import dataclass

# --- Material (atributos visuales) ---
@dataclass
class Material:
    fill_color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    stroke_color: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    stroke_width: float = 1.0


# --- Polyline: base geométrica ---
class Polyline:
    def __init__(self, vertices: np.ndarray, gl_mode: int, material: Material | None = None):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.material = material or Material()
        self.gl_mode = gl_mode

    @property
    def flat_vertices(self) -> np.ndarray:
        """Vertices planos en float32"""
        return self.vertices.flatten().astype('f4')

    @property
    def buffer_data(self) -> bytes:
        """Bytes listos para subir a GPU (solo geometría)."""
        return self.flat_vertices.tobytes()


# --- Mesh: agrega topología ---
class Mesh(Polyline):
    def __init__(self, vertices: np.ndarray, gl_mode: int, indices: np.ndarray, material: Material | None = None):
        super().__init__(vertices, gl_mode, material)
        self.indices = np.array(indices, dtype=np.int32)

    @property
    def flat_indices(self) -> np.ndarray:
        return self.indices.flatten().astype('i4')

    @property
    def vertex_buffer(self) -> bytes:
        """Bytes de vértices listos para buffer."""
        return self.flat_vertices.tobytes()

    @property
    def index_buffer(self) -> bytes:
        """Bytes de índices listos para buffer."""
        return self.flat_indices.tobytes()


# --- Figura derivada: Círculo ---
class CircleMesh(Mesh):
    def __init__(self, radius=1.0, segments=64, gl_mode=4, material: Material | None = None):
        # Calcular vértices
        angles = np.linspace(0, 2 * np.pi, segments, endpoint=False)
        vertices = np.stack([np.cos(angles) * radius, np.sin(angles) * radius], axis=1)
        vertices = np.vstack([[0.0, 0.0], vertices])  # centro + borde
        # Conectividad (triángulos en abanico)
        indices = []
        for i in range(1, segments):
            indices.extend([0, i, i + 1])
        indices.extend([0, segments, 1])  # cerrar círculo

        super().__init__(vertices, gl_mode, np.array(indices), material)
