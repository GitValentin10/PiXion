import numpy as np
import numpy.testing as npt

from camera import Camera


def make_camera():
    projection = np.eye(4, dtype=np.float32)
    return Camera(
        position=(0.0, 0.0, 3.0),
        target=(0.0, 0.0, 0.0),
        theta=0.0,
        aspect_ratio=16 / 9,
        projection_matrix=projection,
    )


def test_camera_basis_vectors_are_orthogonal():
    cam = make_camera()
    npt.assert_allclose(np.dot(cam.camera_x, cam.camera_y), 0.0, atol=1e-5)
    npt.assert_allclose(np.dot(cam.camera_y, cam.camera_z), 0.0, atol=1e-5)


def test_camera_matrix_shape_and_dtype():
    cam = make_camera()
    mat = cam.camera_matrix
    assert mat.shape == (4, 4)
    assert mat.dtype == np.float32


def test_camera_radius_setter_preserves_direction():
    cam = make_camera()
    original_dir = cam.position / np.linalg.norm(cam.position)
    cam.camera_radius = 10.0
    npt.assert_allclose(np.linalg.norm(cam.position), 10.0)
    npt.assert_allclose(cam.position / np.linalg.norm(cam.position), original_dir)


def test_camera_move_translates_position_and_target():
    cam = make_camera()
    cam.move((1.0, 2.0, 3.0))
    npt.assert_allclose(cam.position, np.array([1.0, 2.0, 6.0], dtype=np.float32))
    npt.assert_allclose(cam.target, np.array([1.0, 2.0, 3.0], dtype=np.float32))
