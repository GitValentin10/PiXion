import numpy as np
from utils import normalize


# Cámara orbital con sistema Z-up y matrices compatibles con OpenGL.
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
        # Inicializa posición, objetivo y matrices base para la cámara.
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.theta = theta
        self.aspect_ratio = aspect_ratio
        if projection_matrix is None:
            self.projection_matrix = np.eye(4, dtype=np.float32)
        else:
            self.projection_matrix = np.array(projection_matrix, dtype=np.float32)

    
    @property
    def opengl_swap(self) -> np.ndarray:
        # Matriz de cambio de base entre Z-up propio y convención OpenGL.
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
        # Vector forward normalizado (hacia el objetivo).
        return normalize(self.target - self.position)

    @property
    def camera_z(self) -> np.ndarray:
        # Vector up ortogonal ajustado según la orientación actual.
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
        # Vector lateral (right) obtenido del producto cruz.
        
        return normalize(np.cross(self.camera_y, self.camera_z))
    
    @property
    def camera_radius(self):
        # Distancia actual de la cámara al origen.
        radius = np.linalg.norm(self.position)
        return radius

    @property
    def camera_polar(self):
        # Ángulo polar en coordenadas esféricas.
        polar_angle = np.arccos(self.position[2] / self.camera_radius)
        return polar_angle

    @property
    def camera_azimuthal(self):
        # Ángulo azimutal proyectado sobre el plano XY.
        plane_norm = np.linalg.norm(self.position[:2])
        if plane_norm == 0.0:
            return 0.0
        return np.sign(self.position[1]) * np.arccos(self.position[0] / plane_norm)
    
    @camera_radius.setter
    def camera_radius(self, r: float):
        # Escala la posición manteniendo la dirección actual.
        self.position = normalize(self.position) * r
    
    @camera_polar.setter
    def camera_polar(self, theta: float):
        # Reconstruye coordenadas cartesianas a partir del nuevo polar.
        x = self.camera_radius * np.sin(theta) * np.cos(self.camera_azimuthal)
        y = self.camera_radius * np.sin(theta) * np.sin(self.camera_azimuthal)
        z = self.camera_radius * np.cos(theta)
        self.position = np.array([x, y, z], dtype=np.float32)

    @camera_azimuthal.setter
    def camera_azimuthal(self, phi: float):
        # Ajusta la rotación alrededor del eje vertical conservando radio y polar.
        x = self.camera_radius * np.sin(self.camera_polar) * np.cos(phi)
        y = self.camera_radius * np.sin(self.camera_polar) * np.sin(phi)
        z = self.camera_radius * np.cos(self.camera_polar)
        self.position = np.array([x, y, z], dtype=np.float32)

    @property
    def aspect_ratio_matrix(self) -> float:
        # Matriz que corrige distorsión cuando la ventana no es cuadrada.
        f1 = np.array([1/self.aspect_ratio, 0.0, 0.0, 0.0], dtype=np.float32)
        f2 = np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)
        f3 = np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32)
        f4 = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
        return np.vstack([f1, f2, f3, f4], dtype=np.float32)

    @property
    def view_matrix(self) -> np.ndarray:
        # Construye la matriz look-at basada en los ejes canónicos.
        """Matriz de vista (look-at) calculada a partir de posición y orientación."""
        f1 = np.append(self.camera_x, -self.camera_x @ self.position)
        f2 = np.append(self.camera_y, -self.camera_y @ self.position)
        f3 = np.append(self.camera_z, -self.camera_z @ self.position)
        f4 = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
        return np.vstack([f1, f2, f3, f4], dtype=np.float32)
    
    @property
    def camera_matrix(self) -> np.ndarray:
        # Composición final lista para subir como uniform.
        """Matriz view-projection en formato opengl bytes lista para subir al shader (transpuesta)."""
        return (self.opengl_swap @ self.projection_matrix @ self.aspect_ratio_matrix @ self.view_matrix).astype('f4')


    # --- Transformaciones ---
    def move(self, delta):
        # Traslada posición y objetivo de la cámara en bloque.
        """Desplaza la cámara (en coordenadas del mundo)."""
        delta = np.array(delta, dtype=np.float32)
        self.position += delta
        self.target += delta

    def look_at(self, target):
        # Reapunta la cámara a un nuevo objetivo sin mover la posición.
        """Reorienta la cámara hacia un nuevo objetivo."""
        self.target = np.array(target, dtype=np.float32)
