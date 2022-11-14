#version 330

#if defined VERTEX_SHADER

uniform mat4 m_proj;
uniform mat4 m_cam;
uniform float scale;
in vec3 in_position;
in vec2 in_uv;

out vec2 uv;

void main()
{
    uv = in_uv;
    vec3 pos = in_position * scale + vec3(0, 0, -5);    // add offset
    gl_Position = m_proj * m_cam * vec4(pos, 1.0);
}


#elif defined FRAGMENT_SHADER

uniform sampler2D image;
in vec2 uv;

out vec4 f_color;

void main() {
    f_color = texture(image, uv);
}

#endif
