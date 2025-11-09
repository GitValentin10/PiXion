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
                 aspect_ratio: float = 16 / 9,
                 projection_matrix: np.ndarray | None = None):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.theta = theta
        self.aspect_ratio = aspect_ratio
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
        z_dot_y = z @ self.camera_y

        if z_dot_y == 0.0:
            return np.array([0.0, 0.0, 1.0], dtype=np.float32)
        elif z_dot_y == 1.0:
            return np.array([0.0, -1.0, 0.0], dtype=np.float32)
        elif z_dot_y == -1.0:
            return np.array([0.0, 1.0, 0.0], dtype=np.float32)
        else:
            z_proj_f = (z_dot_y) * self.camera_y
            z_ortho = z - z_proj_f
            return normalize(z_ortho)

    @property
    def camera_x(self) -> np.ndarray:
        
        return normalize(np.cross(self.camera_y, self.camera_z))
    
    @property
    def camera_radius(self):
        radius = np.linalg.norm(self.position)
        return radius

    @property
    def camera_polar(self):
        print(self.camera_y)
        polar_angle = np.arccos(self.position[2] / self.camera_radius)
        return polar_angle

    @property
    def camera_azimuthal(self):
        plane_norm = np.linalg.norm(self.position[:2])
        if plane_norm == 0.0:
            return 0.0
        return np.sign(self.position[1]) * np.arccos(self.position[0] / plane_norm)
    
    @camera_radius.setter
    def camera_radius(self, r: float):
        self.position = normalize(self.position) * r
    
    @camera_polar.setter
    def camera_polar(self, theta: float):
        x = self.camera_radius * np.sin(theta) * np.cos(self.camera_azimuthal)
        y = self.camera_radius * np.sin(theta) * np.sin(self.camera_azimuthal)
        z = self.camera_radius * np.cos(theta)
        self.position = np.array([x, y, z], dtype=np.float32)

    @camera_azimuthal.setter
    def camera_azimuthal(self, phi: float):
        x = self.camera_radius * np.sin(self.camera_polar) * np.cos(phi)
        y = self.camera_radius * np.sin(self.camera_polar) * np.sin(phi)
        z = self.camera_radius * np.cos(self.camera_polar)
        self.position = np.array([x, y, z], dtype=np.float32)

    @property
    def aspect_ratio_matrix(self) -> float:
        f1 = np.array([1/self.aspect_ratio, 0.0, 0.0, 0.0], dtype=np.float32)
        f2 = np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)
        f3 = np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32)
        f4 = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
        return np.vstack([f1, f2, f3, f4], dtype=np.float32)

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
        return (self.opengl_swap @ self.projection_matrix @ self.aspect_ratio_matrix @ self.view_matrix).astype('f4')


    # --- Transformaciones ---
    def move(self, delta):
        """Desplaza la cámara (en coordenadas del mundo)."""
        delta = np.array(delta, dtype=np.float32)
        self.position += delta
        self.target += delta

    def look_at(self, target):
        """Reorienta la cámara hacia un nuevo objetivo."""
        self.target = np.array(target, dtype=np.float32)