#version 330 core

in vec2 frag_pos; // Coordenadas del fragmento en espacio local

uniform vec4 color; // Color del rectángulo (RGBA)
uniform float radius; // Radio de redondeo en las esquinas
uniform vec2 dimensions; // Dimensiones del rectángulo (ancho, alto)

out vec4 FragColor; // Color final del fragmento

void main() {
    vec2 abs_pos = abs(frag_pos); // Valor absoluto de la posición (trabajamos con un cuadrante y reflejamos)
    
    vec2 rect_half_size = dimensions * 0.5; // Mitad de las dimensiones (para trabajar desde el centro)
    
    // Distancia desde el fragmento hasta la zona donde comienza el redondeo en cada eje
    vec2 corner_dist = abs_pos - (rect_half_size - radius);
    
    // Si estamos dentro del área rectangular plana (no en zona de esquinas redondeadas)
    if (corner_dist.x < 0.0 || corner_dist.y < 0.0) {
        FragColor = color; // Dibujamos el color directamente
        return;
    }
    
    // Calculamos la distancia euclidiana al centro del círculo de la esquina
    float dist = length(corner_dist) - radius;
    
    // Aplicamos suavizado para antialiasing en el borde circular
    float alpha = 1.0 - smoothstep(-0.01, 0.01, dist);
    
    // Descartamos fragmentos fuera del borde redondeado (optimización)
    if (alpha < 0.01) discard;
    
    // Aplicamos el alpha calculado para bordes suaves
    FragColor = vec4(color.rgb, color.a * alpha);
}