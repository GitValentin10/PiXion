import numpy as np
import moderngl
import logging
from ..core.geometry import Mesh
from ..core.models import Material, RenderProperties

logger = logging.getLogger(__name__)

# Superficie parametrizada que evalúa una ecuación z=f(x,y).
class Equation3dMesh(Mesh):
    def __init__(self, material: Material, equation_func: callable, rows: int, cols: int):
        # Discretiza la ecuación y construye buffers y shaders apropiados.
        self.vertices, z_meta = self.generate_vertices(equation_func, rows, cols)
        self.indices = self.generate_indices(rows, cols)
        self.render_properties = RenderProperties(
            vertex_shader_path="shaders/equation3dmesh/vertex.glsl",
            fragment_shader_path="shaders/equation3dmesh/fragment.glsl",
            gl_mode=moderngl.TRIANGLES,
            uniforms=[
                {"name": "z_min", "value": z_meta["z_min"]},
                {"name": "z_max", "value": z_meta["z_max"]},
                {"name": "z_span", "value": z_meta["z_span"]},
            ],
        )
        super().__init__(self.vertices, self.indices, material, self.render_properties)

    def generate_vertices(self, equation_func: callable, rows: int, cols: int):
        # Evalúa la función en una malla regular para obtener (x,y,z).
        x = np.linspace(-1, 1, cols)
        y = np.linspace(-1, 1, rows)
        X, Y = np.meshgrid(x, y)
        Z = equation_func(X, Y).astype(np.float32)
        z_min = float(np.min(Z))
        z_max = float(np.max(Z))
        z_span = z_max - z_min
        if z_span == 0.0:
            normalized_z = np.zeros_like(Z, dtype=np.float32)
        else:
            z_center = (z_min + z_max) / 2.0
            normalized_z = ((Z - z_center) / (z_span / 2.0)).astype(np.float32)
        logger.debug(
            "Equation3dMesh: rango Z normalizado (min=%s, max=%s, span=%s)",
            z_min,
            z_max,
            z_span,
        )
        vertices = np.column_stack((X.flatten(), Y.flatten(), normalized_z.flatten())).astype('f4')
        return vertices, {"z_min": z_min, "z_max": z_max, "z_span": z_span if z_span != 0.0 else 1.0}
    
    def generate_indices(self, rows: int, cols: int):
        # Construye dos triángulos por celda de la malla regular.
        indices = np.arange(rows * cols, dtype='i4').reshape((rows, cols))
        t1 = indices[:-1, :-1].ravel()
        quad_index = np.column_stack((
            t1,
            t1 + 1,
            t1 + cols,
            t1 + cols + 1,
            t1 + cols,
            t1 + 1
        )).ravel()
        return quad_index


# Cinta 2D extruida a partir de una función y=f(x).
class Equation2dMesh(Mesh):
    def __init__(self, material, equation_func, segments: int):
        # Genera segmentos a lo largo de la curva y arma un TRIANGLE_STRIP.
        self.vertices = self.generate_vertices(equation_func, segments)
        self.indices = np.arange(len(self.vertices), dtype='i4')
        self.render_properties = RenderProperties(
            vertex_shader_path="shaders/equation2dmesh/vertex.glsl",
            fragment_shader_path="shaders/equation2dmesh/fragment.glsl",
            gl_mode=moderngl.TRIANGLE_STRIP
        )
        super().__init__(self.vertices, self.indices, material, self.render_properties)

    def generate_vertices(self, equation_func, segments: int):
        # Calcula normales laterales para dar grosor a la curva plot.
        x = np.linspace(-1, 1, segments+1)
        y = equation_func(x)
        z = np.zeros_like(x)

        plot_points = np.column_stack((x, y)).astype('f4')
        direction_vectors = plot_points[1:] - plot_points[:-1]
        direction_vectors /= np.linalg.norm(direction_vectors, axis=1, keepdims=True)
        normal_vectors = np.array([-direction_vectors[:,1], direction_vectors[:,0]]).T

        up_points = plot_points[:-1] + normal_vectors * 0.02
        up_vertices = np.column_stack([up_points[:,0], up_points[:,1], z[:-1]]).astype('f4')

        down_points = plot_points[:-1] - normal_vectors * 0.02
        down_vertices = np.column_stack([down_points[:,0], down_points[:,1], z[:-1]]).astype('f4')

        vertices = np.column_stack([up_vertices, down_vertices]).astype('f4')
        return vertices.reshape(-1, 3)
