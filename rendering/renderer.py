import numpy as np
import moderngl
from typing import Tuple, Optional
from ..core.geometry import Mesh
from ..core.camera import Camera
from .shader import ShaderWrapper

# Coordina ModernGL para dibujar las mallas registradas.
class Renderer:
    """Manage a ModernGL pipeline to draw multiple 2D elements."""
    vbos: Optional[list[moderngl.Buffer]]
    ibos: Optional[list[moderngl.Buffer]]
    vaos: Optional[list[moderngl.VertexArray]]

    def __init__(
        self,
        wnd_size: Tuple[int, int],
        models: Optional[list[Mesh]] = None,
        background_color: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0),
        ctx: Optional[moderngl.Context] = None,
        camera: Optional[Camera] = None,
    ) -> None:
        # Prepara buffers, shaders y VAOs correspondientes a cada mesh recibido.
        self.background_color = tuple(background_color)
        self.models = list(models) if models else []
        self.wnd_size = wnd_size
        self.ctx = ctx or moderngl.create_standalone_context()
        aspect_ratio = (wnd_size[0] / wnd_size[1]) if wnd_size[1] else 1.0
        if camera is None:
            default_projection = np.eye(4, dtype=np.float32)
            self.camera = Camera(
                position=np.array([0.0, 0.0, 1.0], dtype=np.float32),
                target=np.array([0.0, 0.0, 0.0], dtype=np.float32),
                theta=0.0,
                aspect_ratio=aspect_ratio,
                projection_matrix=default_projection,
            )
        else:
            self.camera = camera

        self.vbos: list[moderngl.Buffer] = []
        self.ibos: list[moderngl.Buffer] = []
        self.shaders: list[ShaderWrapper] = []
        self.vaos = []

        for mesh in self.models:
            vbo = self.ctx.buffer(mesh.vertex_buffer)
            ibo = self.ctx.buffer(mesh.index_buffer)
            shader = ShaderWrapper(
                self.ctx,
                mesh.render_properties.vertex_shader_path,
                mesh.render_properties.fragment_shader_path,
            )

            for uniform in mesh.render_properties.uniforms:
                shader.program[uniform['name']].value = uniform['value']

            vao = self.ctx.vertex_array(
                shader.program,
                [(vbo, '3f', 'in_pos')],
                ibo,
            )

            self.vbos.append(vbo)
            self.ibos.append(ibo)
            self.shaders.append(shader)
            self.vaos.append(vao)

    
    def render(self) -> None:
        # Configura el viewport, limpia y emite draw calls para cada VAO.
        width, height = self.wnd_size
        self.ctx.viewport = (0, 0, width, height)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(*self.background_color, depth=1.0)
        # Enviar matriz de proyección al shader

        for i, vao in enumerate(self.vaos):
            model = self.models[i]
            self.shaders[i].program['camera_matrix'].write(self.camera.camera_matrix.astype('f4').T.tobytes())

            vao.render(mode=model.render_properties.gl_mode)
