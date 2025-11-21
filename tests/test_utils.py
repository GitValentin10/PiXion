import numpy as np
from pathlib import Path

from utils import normalize, ortho_proj_matrix, perspective_proj_matrix, to_tuple, load_config


def test_normalize_returns_unit_vector():
    vec = np.array([3.0, 4.0, 0.0], dtype=np.float32)
    normalized = normalize(vec)
    assert np.isclose(np.linalg.norm(normalized), 1.0)
    # dirección debe preservarse proporcionalmente
    assert np.allclose(normalized, vec / np.linalg.norm(vec))


def test_normalize_zero_vector_returns_same():
    vec = np.zeros(3, dtype=np.float32)
    assert np.allclose(normalize(vec), vec)


def test_ortho_proj_matrix_shape_and_values():
    mat = ortho_proj_matrix(span=2.0, near=0.5, far=5.5)
    assert mat.shape == (4, 4)
    # elemento [0,0] debe ser 1/span
    assert np.isclose(mat[0, 0], 0.5)
    # fila de traslación en Z debe depender de near/far
    assert np.isclose(mat[1, 3], (-2 * 0.5 / (5.0)) - 1)


def test_perspective_proj_matrix_symmetry():
    mat = perspective_proj_matrix(fov_y=np.radians(60.0), near=0.5, far=5.0)
    assert mat.shape == (4, 4)
    # La matriz debe ser diagonal en los ejes X y Z dado el diseño actual
    assert mat[0, 1] == mat[1, 0] == 0.0
    assert mat[0, 0] > 0 and mat[2, 2] > 0


def test_to_tuple_handles_none_and_sequences():
    assert to_tuple(None, (1, 2)) == (1, 2)
    assert to_tuple([3, 4], (0, 0)) == (3, 4)
    assert to_tuple((5, 6), (0, 0)) == (5, 6)


def test_load_config_reads_toml(tmp_path: Path):
    cfg_path = tmp_path / "config.toml"
    cfg_path.write_text("value = 42\n", encoding="utf-8")
    data = load_config(cfg_path)
    assert data["value"] == 42


def test_load_config_missing_returns_empty(tmp_path: Path):
    assert load_config(tmp_path / "missing.toml") == {}
