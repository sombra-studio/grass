#version 330

#if defined VERTEX_SHADER

uniform mat4 m_proj;
uniform mat4 m_cam;
uniform float scale;
in vec3 in_position;
in vec2 in_uv;
in vec3 in_offset;

out vec2 uv;

void main()
{
    uv = in_uv;
    vec3 pos = in_position * scale + in_offset;    // add offset
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
