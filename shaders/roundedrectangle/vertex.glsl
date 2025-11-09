#version 330 core

layout(location = 0) in vec3 in_pos;

uniform mat4 camera_matrix;

out vec2 frag_pos;

void main() {
    frag_pos = in_pos.xy;
    gl_Position = camera_matrix * vec4(in_pos, 1.0);
}