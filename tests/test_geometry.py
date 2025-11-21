import numpy as np

from geometry import Material, RenderProperties, Polyline, Mesh


def make_render_props():
    return RenderProperties(
        vertex_shader_path="shaders/dummy.vert",
        fragment_shader_path="shaders/dummy.frag",
        gl_mode=4,
        uniforms=[{"name": "color", "value": (1.0, 0.0, 0.0, 1.0)}],
    )


def test_material_defaults_are_clamped():
    mat = Material()
    assert mat.fill_color == (1.0, 1.0, 1.0, 1.0)
    assert mat.stroke_color[3] == 1.0


def test_polyline_buffers_flatten_vertices():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], dtype=np.float32)
    poly = Polyline(vertices, Material(), make_render_props())
    flattened = poly.flat_vertices
    assert flattened.shape == (6,)
    assert poly.buffer_data == flattened.tobytes()


def test_mesh_buffers_use_indices():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32)
    indices = np.array([0, 1, 2], dtype=np.int32)
    mesh = Mesh(vertices, indices, Material(), make_render_props())
    assert mesh.flat_indices.tolist() == [0, 1, 2]
    assert len(mesh.index_buffer) == indices.size * indices.dtype.itemsize
    assert len(mesh.vertex_buffer) == vertices.size * vertices.dtype.itemsize
