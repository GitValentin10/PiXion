import numpy as np
from .models import Material, RenderProperties

# --- Polyline: base geométrica ---
# Envuelve una lista de vértices y los materiales asociados.
class Polyline:
    def __init__(self, vertices: np.ndarray, material: Material, render_properties: RenderProperties):
        # Copia los vértices como float32 y almacena config visual y de shaders.
        self.vertices = np.array(vertices, dtype=np.float32)
        self.material = material or Material()
        self.render_properties = render_properties

    @property
    def flat_vertices(self) -> np.ndarray:
        # Devuelve arreglo 1D listo para buffers.
        """Vertices planos en float32"""
        return self.vertices.flatten().astype('f4')

    @property
    def buffer_data(self) -> bytes:
        # Serializa los vértices para subirlos a la GPU.
        """Bytes listos para subir a GPU (solo geometría)."""
        return self.flat_vertices.tobytes()


# --- Mesh: agrega topología ---
# Especializa Polyline con índices para dibujar triángulos o tiras.
class Mesh(Polyline):
    def __init__(self, vertices: np.ndarray, indices: np.ndarray, material: Material, render_properties: RenderProperties):
        super().__init__(vertices, material, render_properties)
        self.indices = np.array(indices, dtype=np.int32)

    @property
    def flat_indices(self) -> np.ndarray:
        # Indices lineales listos para el IBO.
        return self.indices.flatten().astype('i4')

    @property
    def vertex_buffer(self) -> bytes:
        # Paquete de vértices para buffer de posición.
        """Bytes de vértices listos para buffer."""
        return self.flat_vertices.tobytes()

    @property
    def index_buffer(self) -> bytes:
        # Paquete de índices para buffer de elementos.
        """Bytes de índices listos para buffer."""
        return self.flat_indices.tobytes()
