#version 330 core

in vec3 in_pos;
uniform mat4 camera_matrix;

void main() {
    gl_Position = camera_matrix * vec4(in_pos, 1.0);
}
