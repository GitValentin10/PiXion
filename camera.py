import numpy as np
from utils import normalize


class Camera:
# Cámara en sistema Z-up (Right-Handed):
#  - Z = arriba, Y = adelante, X = derecha
#  - Usa convención cartesiana clásica
#  - La vista y proyección toman Y como eje de profundidad

    def __init__(self,
                 position,
                 target,
                 theta,
                 projection_matrix: np.ndarray | None = None):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.theta = theta
        self.projection_matrix = projection_matrix.astype(np.float32)
    
    @property
    def opengl_swap(self) -> np.ndarray:
        """
        Matriz de transformación de ejes:
        Convierte de sistema Z-up (x, y, z)
        a sistema OpenGL (x, z, y) y viceversa.
        """
        row1 = np.array([1, 0, 0, 0], dtype=np.float32)  # X -> X
        row2 = np.array([0, 0, 1, 0], dtype=np.float32)  # Z -> Y (vertical)
        row3 = np.array([0, 1, 0, 0], dtype=np.float32)  # Y -> Z (profundidad)
        row4 = np.array([0, 0, 0, 1], dtype=np.float32)
        return np.vstack([row1, row2, row3, row4])

    # --- Ejes ortogonales camara ---
    @property
    def camera_y(self) -> np.ndarray:
        return normalize(self.target - self.position)

    @property
    def camera_z(self) -> np.ndarray:
        z = np.array([0.0, 0.0, 1.0], dtype=np.float32)
        z_proj_f = (z @ self.camera_y) * self.camera_y
        z_theta_0 = normalize(z - z_proj_f)
        x_theta_0 = normalize(np.cross(self.camera_y, z_theta_0))
        z_rotated = x_theta_0 * np.sin(self.theta) + z_theta_0 * np.cos(self.theta)
        return z_rotated

    @property
    def camera_x(self) -> np.ndarray:
        return normalize(np.cross(self.camera_y, self.camera_z))


    @property
    def view_matrix(self) -> np.ndarray:
        """Matriz de vista (look-at) calculada a partir de posición y orientación."""
        f1 = np.append(self.camera_x, -self.camera_x @ self.position)
        f2 = np.append(self.camera_y, -self.camera_y @ self.position)
        f3 = np.append(self.camera_z, -self.camera_z @ self.position)
        f4 = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
        return np.vstack([f1, f2, f3, f4], dtype=np.float32)
    
    @property
    def camera_matrix(self) -> np.ndarray:
        """Matriz view-projection en formato opengl bytes lista para subir al shader (transpuesta)."""
        return (self.opengl_swap @ self.projection_matrix @ self.view_matrix @ self.opengl_swap).astype('f4')


    # --- Transformaciones ---
    def move(self, delta):
        """Desplaza la cámara (en coordenadas del mundo)."""
        delta = np.array(delta, dtype=np.float32)
        self.position += delta
        self.target += delta

    def look_at(self, target):
        """Reorienta la cámara hacia un nuevo objetivo."""
        self.target = np.array(target, dtype=np.float32)