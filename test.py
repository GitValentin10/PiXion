import numpy as np
from app import OpenWindow
from render import Renderer
from camera import Camera
from utils import ortho_proj_matrix, perspective_proj_matrix
import moderngl_window as mglw
from geometry import Material
from models import Equation2dMesh, Equation3dMesh, RoundedRectangle
import matplotlib.pyplot as plt

if __name__ == "__main__":

    material = Material(
        fill_color=(1.0, 1.0, 1.0, 1.0),
        stroke_color=(0.0, 0.0, 0.0, 1.0),
        stroke_width=2.0,
    )

    def equation_func(x, y):
        # Superficie de referencia para probar Equation3dMesh.
        return np.exp((x**2 + y**2))

    def equation_func_2d(x):
        # Curva simple para la prueba 2D.
        return x**2

    window = mglw.create_window_config_instance(OpenWindow)
    aspect_ratio = window.wnd.size[0] / window.wnd.size[1]
    ortho_projection_matrix = ortho_proj_matrix(
        span=3.0,
        near=0.1,
        far=10.0
    )
    test_matrix = perspective_proj_matrix(
        fov_y=np.radians(30.0),
        near=0.1,
        far=100.0
    )
    models = [
        RoundedRectangle(
            material=material,
            width=2.0,
            height=1.0,
            radius=0.1
        )

    ]
    
    camera = Camera(
        position=(0.0, 3.0, 2.0),
        target=(0.0, 0.0, 0.0),
        theta=0.0,
        aspect_ratio=aspect_ratio,
        projection_matrix=test_matrix,
    )
    renderer = Renderer(
        wnd_size=window.wnd.size,
        models=models,
        background_color=(0.1, 0.1, 0.1, 1.0),
        camera=camera,
        ctx=window.ctx,
        )
    np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    print(camera.camera_x)
    print(camera.camera_y)
    print(camera.camera_z)
    print(camera.view_matrix@ np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float32))
    window.set_renderer(renderer)
    mglw.run_window_config_instance(window)
