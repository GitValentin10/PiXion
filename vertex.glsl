#version 330 core

in vec2 in_pos;
uniform mat4 projection;

void main() {
    gl_Position = projection * vec4(in_pos, 1.0, 1.0);
}
