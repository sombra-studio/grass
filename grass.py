from array import array
import moderngl
import moderngl_window


class Grass:
    def __init__(self, window: moderngl_window.WindowConfig):
        self.diffuse = window.load_texture_2d('data/base_grass5.png')
        self.vbo = window.ctx.buffer(
            array(
                'f',
                [
                    # Triangle strip creating a plane
                    # x, y, z, u, v
                    -150, -2, -300, 0, 0,      # lower left
                    -150, -2, 0, 0, 1,    # upper left
                    150, -2, -300, 1, 0,      # lower right
                    150, -2, 0, 1, 1     # upper right
                ]
            )
        )
        self.program = window.load_program('shaders/terrain.glsl')
        self.vao = window.ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f 2f', 'in_position', 'in_uv'),
            ]
        )
        self.window = window

    def draw(self, projection_matrix=None, camera_matrix=None, time=0.0):
        self.program["m_proj"].write(projection_matrix)
        self.program["m_cam"].write(camera_matrix)
        self.diffuse.use(0)
        self.vao.render(moderngl.TRIANGLE_STRIP)