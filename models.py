from geometry import Mesh, Material, RenderProperties
import numpy as np
import moderngl

class Equation3dMesh(Mesh):
    def __init__(self, material: Material, equation_func: callable, rows: int, cols: int):
        self.vertices = self.generate_vertices(equation_func, rows, cols)
        self.indices = self.generate_indices(rows, cols)
        self.render_properties = RenderProperties(
            vertex_shader_path="shaders/equation3dmesh/vertex.glsl",
            fragment_shader_path="shaders/equation3dmesh/fragment.glsl",
            gl_mode=moderngl.TRIANGLES
            )
        super().__init__(self.vertices, self.indices, material, self.render_properties)

    def generate_vertices(self, equation_func: callable, rows: int, cols: int):
        x = np.linspace(-1, 1, cols)
        y = np.linspace(-1, 1, rows)
        X, Y = np.meshgrid(x, y)
        Z = equation_func(X, Y)
        vertices = np.column_stack((X.flatten(), Y.flatten(), Z.flatten())).astype('f4')
        print(max(vertices[:,2]), min(vertices[:,2]))
        return vertices
    
    def generate_indices(self, rows: int, cols: int):
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

class RoundedRectangle(Mesh):
    def __init__(self, material: Material, width: float, height: float, radius: float):
        self.vertices = self.generate_vertices(width, height)
        self.indices = self.generate_indices()
        self.render_properties = RenderProperties(
            vertex_shader_path="shaders/roundedrectangle/vertex.glsl",
            fragment_shader_path="shaders/roundedrectangle/fragment.glsl",
            uniforms=[{
                "name": "color",
                "type": "vec4",
                "value": material.fill_color
            },
            {
                "name": "radius",
                "type": "float",
                "value": radius
            },
            {
                "name": "dimensions",
                "type": "vec2",
                "value": np.array([width, height], dtype='f4')
            }],
            gl_mode=moderngl.TRIANGLES
        )
        super().__init__(self.vertices, self.indices, material, self.render_properties)
    
    def generate_vertices(self, width: float, height: float):
        v1 = np.array([-(width/2), -(height/2), 0.0], dtype='f4')
        v2 = np.array([ (width/2), -(height/2), 0.0], dtype='f4')
        v3 = np.array([ (width/2),  (height/2), 0.0], dtype='f4')
        v4 = np.array([-(width/2),  (height/2), 0.0], dtype='f4')
        return np.array([v1, v2, v3, v4], dtype='f4')

    def generate_indices(self):
        return np.array([0, 1, 2, 2, 3, 0], dtype='i4')


class Equation2dMesh(Mesh):
    def __init__(self, material, equation_func, segments: int):
        self.vertices = self.generate_vertices(equation_func, segments)
        self.indices = np.arange(len(self.vertices), dtype='i4')
        self.render_properties = RenderProperties(
            vertex_shader_path="shaders/equation2dmesh/vertex.glsl",
            fragment_shader_path="shaders/equation2dmesh/fragment.glsl",
            gl_mode=moderngl.TRIANGLE_STRIP
        )
        super().__init__(self.vertices, self.indices, material, self.render_properties)

    def generate_vertices(self, equation_func, segments: int):
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