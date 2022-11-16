#version 330

#if defined VERTEX_SHADER

uniform mat4 m_proj;
uniform mat4 m_cam;
uniform float scale;
uniform float time;
uniform float grid_size;
uniform sampler2D noise;
in vec3 in_position;
in vec2 in_texcoord;
in vec3 in_offset;

out vec2 texcoord;

void main()
{
    texcoord = in_texcoord;
    float s_noise = (in_offset.x + grid_size / 2) / (grid_size * 4);
    float t_noise = (-in_offset.z) / (grid_size * 4);
    float local_wind_factor = texture(noise, vec2(s_noise, t_noise)).x;
    float wind_drag = (
        0.2 * sin(time + 6 * s_noise) * in_texcoord.t * local_wind_factor
    );
    vec3 pos = in_position * scale + in_offset + vec3(wind_drag, 0, 0);
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
