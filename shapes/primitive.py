import numpy as np
import moderngl
from ..core.geometry import Mesh
from ..core.models import Material, RenderProperties

# Malla rectangular simple con esquinas redondeadas controladas en shader.
class RoundedRectangle(Mesh):
    def __init__(self, material: Material, width: float, height: float, radius: float):
        # Define cuatro vértices y uniforms necesarios para el shader.
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
        # Devuelve el rectángulo centrado en origen.
        v1 = np.array([-(width/2), -(height/2), 0.0], dtype='f4')
        v2 = np.array([ (width/2), -(height/2), 0.0], dtype='f4')
        v3 = np.array([ (width/2),  (height/2), 0.0], dtype='f4')
        v4 = np.array([-(width/2),  (height/2), 0.0], dtype='f4')
        return np.array([v1, v2, v3, v4], dtype='f4')

    def generate_indices(self):
        # Usa dos triángulos para cubrir el rectángulo.
        return np.array([0, 1, 2, 2, 3, 0], dtype='i4')
