import moderngl_window as mglw
import numpy as np
import moderngl_window as mglw
import numpy as np
from app.window import OpenWindow
from rendering.renderer import Renderer
from core.models import Material
from shapes.equation import Equation3dMesh
from utils.math import perspective_proj_matrix

def main():
    # Configuración inicial de la ventana
    window_cls = OpenWindow
    mglw.run_window_config(window_cls)

    # Nota: mglw.run_window_config toma control del loop principal.
    # Para inyectar el renderer, necesitamos hacerlo dentro de la clase Window o
    # usar un patrón diferente si queremos instanciarlo fuera.
    # Sin embargo, mglw instancia la clase Window por nosotros.
    # Una forma común es inicializar cosas en el __init__ de la ventana.
    # Pero aquí OpenWindow espera un set_renderer.
    
    # Revisando como funciona mglw, normalmente se sobreescribe __init__ en la clase WindowConfig.
    # Pero para mantener la estructura anterior donde 'test.py' o similar configuraba el renderer:
    
    # Vamos a modificar OpenWindow para que pueda inicializar un renderer por defecto o 
    # permitir configuración.
    # Dado que estamos refactorizando, lo ideal es que OpenWindow se encargue de su setup 
    # o que usemos un timer/evento para configurarlo, pero mglw es algo restrictivo.
    
    # La mejor opción para este refactor rápido es que OpenWindow cree su propio Renderer de prueba
    # si no se le pasa uno (lo cual es difícil porque mglw la instancia).
    # O mejor, movemos la lógica de creación de escena dentro de OpenWindow.__init__ 
    # o un método on_init.
    
    pass

# Re-writing main logic to be compatible with mglw structure
# We need to subclass OpenWindow in main.py or inject logic.
class Application(OpenWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Scene Setup
        material = Material(fill_color=(1.0, 0.5, 0.2, 1.0))
        
        def sombrero(x, y):
            r = np.sqrt(x**2 + y**2)
            return np.sin(r) / (r + 0.001)

        mesh = Equation3dMesh(material, sombrero, 50, 50)
        
        # Camera Setup
        aspect = self.window_size[0] / self.window_size[1]
        proj = perspective_proj_matrix(np.radians(45.0), 0.1, 100.0)
        
        # Renderer Setup
        self.renderer = Renderer(
            wnd_size=self.window_size,
            models=[mesh],
            ctx=self.ctx,
            camera=None # Renderer creates default camera
        )
        self.renderer.camera.projection_matrix = proj
        self.renderer.camera.position = np.array([3.0, 3.0, 3.0], dtype=np.float32)
        self.renderer.camera.look_at([0.0, 0.0, 0.0])

if __name__ == '__main__':
    mglw.run_window_config(Application)
