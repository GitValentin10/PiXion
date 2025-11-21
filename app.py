from pathlib import Path
from typing import Tuple
from utils import to_tuple, load_config
import moderngl_window as mglw
from render import Renderer
import numpy as np



Color = Tuple[float, float, float, float]
CONFIG_PATH = Path(__file__).with_name("config.toml")
_CONFIG = load_config(CONFIG_PATH)
_WINDOW_SETTINGS = _CONFIG.get("main_window", {})


# Ventana principal que canaliza eventos hacia un Renderer configurado.
class OpenWindow(mglw.WindowConfig):
    """Basic window that delegates rendering to a Renderer instance."""

    gl_version = to_tuple(_WINDOW_SETTINGS.get("gl_version"), (3, 3))
    title = _WINDOW_SETTINGS.get("title", "Renderer 2D con ModernGL")
    window_size = to_tuple(_WINDOW_SETTINGS.get("window_size"), (1280, 720))
    aspect_ratio = _WINDOW_SETTINGS.get("aspect_ratio", 16 / 9)
    resizable = bool(_WINDOW_SETTINGS.get("resizable", True))
    
    def set_renderer(self, renderer: Renderer) -> None:
        # Guarda la instancia que se encargará de dibujar cada frame.
        self.renderer = renderer

    def on_render(self, time, frame_time) -> None:
        # Ciclo de dibujo: delega en el renderer asociado.
        self.renderer.render()
    
    def on_mouse_scroll_event(self, x_offset, y_offset):
        # Ajusta el radio orbital para acercar o alejar la cámara.
        self.renderer.camera.camera_radius *= (1 + y_offset)
    
    def on_mouse_drag_event(self, x, y, dx, dy):
        # Traducir arrastre a cambios en ángulos azimutal y polar.
        self.renderer.camera.camera_azimuthal -= np.radians(dx * 0.5)
        self.renderer.camera.camera_polar -= np.radians(dy * 0.5)
