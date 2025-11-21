from pydantic import BaseModel, Field
from typing import Optional, Tuple

# --- Material (atributos visuales) ---
# Describe colores básicos y grosor de líneas para una primitiva.
class Material(BaseModel):
    fill_color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    stroke_color: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    stroke_width: Optional[float] = 1.0

# Parametriza shaders, modo GL y uniformes asociados a un mesh.
class RenderProperties(BaseModel):
    vertex_shader_path: str
    fragment_shader_path: str
    gl_mode: Optional[int] = None
    uniforms: list[dict] = Field(default_factory=list)
