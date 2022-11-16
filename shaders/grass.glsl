#version 330

#if defined VERTEX_SHADER

uniform mat4 m_proj;
uniform mat4 m_cam;
uniform float scale;
uniform float wind_move;
in vec3 in_position;
in vec2 in_texcoord;
in vec3 in_offset;

out vec2 texcoord;

void main()
{
    texcoord = in_texcoord;
    float wind_drag = wind_move * in_texcoord.t * sin(gl_InstanceID);
    vec3 pos = in_position * scale + in_offset + vec3(wind_drag, 0, 0);    // add offset
    gl_Position = m_proj * m_cam * vec4(pos, 1.0);
}


#elif defined FRAGMENT_SHADER

uniform sampler2D image;
in vec2 texcoord;

out vec4 f_color;

void main() {
    f_color = texture(image, texcoord);
}

#endif
