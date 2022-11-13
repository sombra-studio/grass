#version 330

#if defined VERTEX_SHADER

uniform mat4 m_proj;
uniform mat4 m_cam;
uniform float uv_scale;
in vec3 in_position;
in vec2 in_uv;

out vec3 v_vert;
out vec2 uv;

void main()
{
    uv = in_uv * uv_scale;
    v_vert = in_position;
    gl_Position = m_proj * m_cam * vec4(in_position, 1.0);
}


#elif defined FRAGMENT_SHADER

uniform sampler2D image;
uniform sampler2D normals;
uniform vec3 light_pos;
in vec2 uv;
in vec3 v_vert;

out vec4 f_color;

void main() {
    vec3 l = normalize(light_pos - v_vert);
    vec3 n = normalize(texture(normals, uv).rbg * 2.0 - 1.0);
    float n_dot_l = clamp(dot(l, n), 0.0, 1.0);
    vec3 diffuse = texture(image, uv).rgb;
    vec3 color = clamp(diffuse * n_dot_l, 0.0, 1.0);
    f_color = vec4(color, 1.0);
}

#endif
