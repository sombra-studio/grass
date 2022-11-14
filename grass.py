from array import array
from math import cos, sin, radians
import moderngl
import moderngl_window


class Grass:
    def __init__(self, window: moderngl_window.WindowConfig):
        self.diffuse = window.load_texture_2d('data/grass3.png')
        sin_theta = sin(radians(45))
        cos_theta = cos(radians(45))
        self.vbo = window.ctx.buffer(
            array(
                'f',
                [
                    # Triangle strip creating a plane
                    # x, y, z, u, v
                    # First plane
                    -1, 0, 0, 0, 0,      # lower left
                    -1, 2, 0, 0, 1,    # upper left
                    1, 0, 0, 1, 0,      # lower right
                    1, 2, 0, 1, 1,     # upper right
                    # Zero area triangle
                    1, 2, 0, 1, 1,
                    -cos_theta, 0, sin_theta, 0, 0,
                    # Second plane
                    -cos_theta, 0, sin_theta, 0, 0,  # lower left
                    -cos_theta, 2, sin_theta, 0, 1,  # upper left
                    cos_theta, 0, -sin_theta, 1, 0,  # lower right
                    cos_theta, 2, -sin_theta, 1, 1,  # upper right
                    # Zero area triangle
                    cos_theta, 2, -sin_theta, 1, 1,
                    -cos_theta, 0, -sin_theta, 0, 0,
                    # Third plane
                    -cos_theta, 0, -sin_theta, 0, 0,  # lower left
                    -cos_theta, 2, -sin_theta, 0, 1,  # upper left
                    cos_theta, 0, sin_theta, 1, 0,  # lower right
                    cos_theta, 2, sin_theta, 1, 1  # upper right
                ]
            )
        )
        self.program = window.load_program('shaders/grass.glsl')
        self.program['scale'].value = 0.5
        self.vao = window.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f 2f', 'in_position', 'in_uv'),
            ]
        )
        self.window = window

    def draw(self, projection_matrix=None, camera_matrix=None):
        self.program["m_proj"].write(projection_matrix)
        self.program["m_cam"].write(camera_matrix)
        self.diffuse.use(0)
        self.vao.render(moderngl.TRIANGLE_STRIP)