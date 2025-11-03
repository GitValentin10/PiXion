import numpy as np
from app import OpenWindow
from render import Renderer, ShaderWrapper
from camera import Camera
from utils import ortho_proj_matrix
import moderngl_window as mglw
from geometry import CircleMesh, Material


if __name__ == "__main__":
    circle_material = Material(
        fill_color=(1.0, 1.0, 1.0, 1.0),
        stroke_color=(0.0, 0.0, 0.0, 1.0),
        stroke_width=2.0,
    )
    meshes = [
        CircleMesh(radius=1, segments=64, gl_mode=4, material=circle_material),
    ]
    
    window = mglw.create_window_config_instance(OpenWindow)
    
    # Crear matriz de proyección ortográfica con aspect ratio correcto
    aspect_ratio = window.wnd.size[0] / window.wnd.size[1]
    projection_matrix = ortho_proj_matrix(
        aspect_ratio=aspect_ratio,
        span=3.0,
        near=0.1,
        far=3.0,
    )
    
    camera = Camera(
        position=(0.0, 0.0, 0.0),
        target=(0.0, 1.0, 0.0),
        theta=0.0,
        projection_matrix=projection_matrix
    )
    renderer = Renderer(
        wnd_size=window.wnd.size,
        meshes=meshes,
        background_color=(0.0, 0.0, 0.0, 1.0),
        shader=ShaderWrapper(window.ctx, "./vertex.glsl", "./fragment.glsl"),
        camera=camera,
        ctx=window.ctx,
        )
    print(camera.camera_matrix @ np.array([0.0, 0.0, -1.0, 1.0], dtype='f4'))
    window.set_renderer(renderer)
    mglw.run_window_config_instance(window)
