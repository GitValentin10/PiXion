from pathlib import Path
from typing import Tuple
import moderngl_window as mglw
import numpy as np
from ..rendering.renderer import Renderer
from ..utils.math import to_tuple
from .config import load_config

Color = Tuple[float, float, float, float]
# Assuming config.toml is at the root or we need to find it relative to this file?
# The original code looked for config.toml next to app.py.
# Now app.py is moved to pyxion/app/window.py.
# We should probably look for config.toml in the project root.
# Let's assume project root is 2 levels up from here.
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.toml"

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
        if hasattr(self, 'renderer'):
            self.renderer.render()
    
    def on_mouse_scroll_event(self, x_offset, y_offset):
        # Ajusta el radio orbital para acercar o alejar la cámara.
        if hasattr(self, 'renderer'):
            self.renderer.camera.camera_radius *= (1 + y_offset)
    
    def on_mouse_drag_event(self, x, y, dx, dy):
        # Traducir arrastre a cambios en ángulos azimutal y polar.
        if hasattr(self, 'renderer'):
            self.renderer.camera.camera_azimuthal -= np.radians(dx * 0.5)
            self.renderer.camera.camera_polar -= np.radians(dy * 0.5)
