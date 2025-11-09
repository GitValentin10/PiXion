import numpy as np
from pydantic import BaseModel
from typing import Optional

# --- Material (atributos visuales) ---
class Material(BaseModel):
    fill_color: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    stroke_color: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    stroke_width: Optional[float] = 1.0

class RenderProperties(BaseModel):
    vertex_shader_path: str
    fragment_shader_path: str
    gl_mode: Optional[int] = None
    uniforms: list[dict] = []


# --- Polyline: base geométrica ---
class Polyline:
    def __init__(self, vertices: np.ndarray, material: Material, render_properties: RenderProperties):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.material = material or Material()
        self.render_properties = render_properties

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
    def __init__(self, vertices: np.ndarray, indices: np.ndarray, material: Material, render_properties: RenderProperties):
        super().__init__(vertices, material, render_properties)
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