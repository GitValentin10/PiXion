# PyXion Architecture

This document outlines the high-level architecture of the PyXion application after refactoring.

## Component Diagram

```mermaid
classDiagram
    class Main {
        +main()
    }

    namespace App {
        class OpenWindow {
            +set_renderer(renderer)
            +on_render()
            +on_mouse_events()
        }
        class Config {
            +load_config()
        }
    }

    namespace Rendering {
        class Renderer {
            +render()
            +vbos
            +ibos
            +vaos
        }
        class ShaderWrapper {
            +program
        }
    }

    namespace Core {
        class Camera {
            +position
            +target
            +view_matrix
            +projection_matrix
        }
        class Mesh {
            +vertices
            +indices
            +material
            +render_properties
        }
        class Polyline {
            +vertices
            +material
        }
        class Material {
            +fill_color
            +stroke_color
        }
        class RenderProperties {
            +vertex_shader_path
            +fragment_shader_path
            +uniforms
        }
    }

    namespace Shapes {
        class Equation3dMesh {
            +generate_vertices()
        }
        class RoundedRectangle {
            +generate_vertices()
        }
    }

    namespace Utils {
        class Math {
            +normalize()
            +perspective_proj_matrix()
        }
    }

    %% Relationships
    Main --> OpenWindow : Instantiates
    Main --> Renderer : Instantiates
    Main --> Equation3dMesh : Creates Scene

    OpenWindow --> Renderer : Delegates Rendering

    Renderer --> Camera : Uses
    Renderer --> Mesh : Renders List of
    Renderer --> ShaderWrapper : Uses

    Mesh --|> Polyline : Inherits
    Mesh *-- Material : Has
    Mesh *-- RenderProperties : Has

    Equation3dMesh --|> Mesh : Inherits
    RoundedRectangle --|> Mesh : Inherits

    Camera ..> Math : Uses
```

## Module Description

- **Core**: Contains the fundamental data structures (`Mesh`, `Material`) and logic (`Camera`) that are independent of the rendering engine or application window.
- **Rendering**: Handles the interaction with ModernGL. The `Renderer` takes `Mesh` objects and draws them using `ShaderWrapper`.
- **Shapes**: Concrete implementations of `Mesh` for specific geometries like mathematical surfaces or UI primitives.
- **App**: Manages the windowing system (using `moderngl_window`) and user input events.
- **Utils**: Pure mathematical helpers and configuration loaders.
