#version 330 core

// Fragment shader with uniform color and a subtle animation
in vec2 v_uv;
out vec4 fragColor;
uniform vec4 color;

void main() {
    fragColor = vec4(color.rgb, color.a);
}
