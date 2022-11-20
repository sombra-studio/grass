from array import array
from math import cos, sin, radians
import moderngl
import moderngl_window
import numpy as np

COLS = 600
ROWS = 600
CELL_SIZE = 0.5
DIFFUSE_MAP_UNIT = 0
NOISE_MAP_UNIT = 1


class Grass:
    def __init__(self, window: moderngl_window.WindowConfig):
        self.diffuse = window.load_texture_2d('data/grass3.png')
        self.diffuse.repeat_x = False
        self.diffuse.repeat_y = False
        self.diffuse.build_mipmaps()
        self.noise = window.load_texture_2d('data/noise.png')
        sin_theta = sin(radians(45))
        cos_theta = cos(radians(45))
        self.ctx = window.ctx
        self.vbo = self.ctx.buffer(
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
        # Create offsets for instances
        offset_x = (
            np.tile(np.arange(COLS) * CELL_SIZE, ROWS) - COLS * CELL_SIZE / 2
        )
        offset_y = np.zeros(ROWS * COLS)
        offset_z = np.repeat(-np.arange(ROWS) * CELL_SIZE, COLS)
        offsets = np.dstack([offset_x, offset_y, offset_z])
        self.vbo_offsets = self.ctx.buffer(offsets.astype('f4'))
        self.program = window.load_program('shaders/grass.glsl')
        self.program['scale'].value = 0.5
        self.program['grid_size'].value = ROWS
        self.program['image'].value = DIFFUSE_MAP_UNIT
        self.program['noise'].value = NOISE_MAP_UNIT
        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f 2f', 'in_position', 'in_texcoord'),
                (self.vbo_offsets, '3f /i', 'in_offset')
            ]
        )
        self.window = window

    def draw(self, projection_matrix=None, camera_matrix=None, time=0.0):
        self.program["m_proj"].write(projection_matrix)
        self.program["m_cam"].write(camera_matrix)
        self.program["time"].value = time
        self.diffuse.use(location=DIFFUSE_MAP_UNIT)
        self.noise.use(location=NOISE_MAP_UNIT)
        self.vao.render(moderngl.TRIANGLE_STRIP, instances=ROWS*COLS)
