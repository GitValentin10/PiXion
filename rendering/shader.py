import moderngl
from pathlib import Path

# Pequeño helper para compilar y manejar pares de shaders.
class ShaderWrapper:
    """
    Envoltura simple para compilar y almacenar un shader program de ModernGL.
    Carga archivos .vert y .frag desde disco y crea el programa al instanciar.
    """
    def __init__(self, ctx: moderngl.Context, vertex_path: str, fragment_path: str):
        # Lee ambos archivos del disco y crea el programa asociado.
        self.ctx = ctx
        self.vertex_path = Path(vertex_path)
        self.fragment_path = Path(fragment_path)

        if not self.vertex_path.exists():
            raise FileNotFoundError(f"Vertex shader no encontrado: {self.vertex_path}")
        if not self.fragment_path.exists():
            raise FileNotFoundError(f"Fragment shader no encontrado: {self.fragment_path}")

        vertex_src = self.vertex_path.read_text(encoding="utf-8")
        fragment_src = self.fragment_path.read_text(encoding="utf-8")
        self.program = self.ctx.program(
            vertex_shader=vertex_src,
            fragment_shader=fragment_src
        )
