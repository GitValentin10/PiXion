import numpy as np
from geometry import Mesh
from camera import Camera
import moderngl
from typing import Tuple, Optional
from pathlib import Path


class ShaderWrapper:
    """
    Envoltura simple para compilar y almacenar un shader program de ModernGL.
    Carga archivos .vert y .frag desde disco y crea el programa al instanciar.
    """
    program: moderngl.Program
    def __init__(self, ctx: moderngl.Context, vertex_path: str, fragment_path: str):
        self.ctx = ctx
        self.vertex_path = Path(vertex_path)
        self.fragment_path = Path(fragment_path)

        if not self.vertex_path.exists():
            raise FileNotFoundError(f"Vertex shader no encontrado: {self.vertex_path}")
        if not self.fragment_path.exists():
            raise FileNotFoundError(f"Fragment shader no encontrado: {self.fragment_path}")

        vertex_src = self.vertex_path.read_text(encoding="utf-8")
        fragment_src = self.fragment_path.read_text(encoding="utf-8")

        # Compilar inmediatamente
        self.program = self.ctx.program(
            vertex_shader=vertex_src,
            fragment_shader=fragment_src
        )


class Renderer:
    """Manage a ModernGL pipeline to draw multiple 2D elements."""
    vbos: Optional[list[moderngl.Buffer]]
    ibos: Optional[list[moderngl.Buffer]]
    vaos: Optional[list[moderngl.VertexArray]]
    def __init__(
        self,
        wnd_size: Tuple[int, int],
        meshes: list[Mesh] = [],
        background_color: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0),
        shader: ShaderWrapper | None = None,
        ctx: Optional[moderngl.Context] = None,
        camera: Optional[Camera] = None,
    ) -> None:
        self.vaos = []
        self.background_color = tuple(background_color)
        self.meshes = meshes
        self.shader = shader
        self.ctx = ctx
        self.wnd_size = wnd_size
        self.camera = camera
        self.vbos = [ctx.buffer(m.vertex_buffer) for m in self.meshes]
        self.ibos = [ctx.buffer(m.index_buffer) for m in self.meshes]
        for vbo, ibo in zip(self.vbos, self.ibos):
            self.vaos.append(
                ctx.vertex_array(
                    self.shader.program,
                    [(vbo, '2f', 'in_pos')],
                    ibo
                )
            )

    
    def render(self) -> None:
        width, height = self.wnd_size
        self.ctx.viewport = (0, 0, width, height)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(*self.background_color, depth=1.0)

        # Enviar matriz de proyección al shader
        self.shader.program['projection'].write(self.camera.camera_matrix.T.tobytes())
        self.shader.program['color'].write(np.array([1.0, 1.0, 1.0, 1.0], dtype='f4').tobytes())

        for i, vao in enumerate(self.vaos):
            mesh = self.meshes[i]
            vao.render(mode=moderngl.TRIANGLES)


