from array import array
import moderngl

DIFFUSE_MAP_UNIT = 0
NORMAL_MAP_UNIT = 1


class Terrain:
    def __init__(self, window):
        """
        Object for a 3D terrain.
        Args:
            window (Window): The window that will display this terrain.
        """
        self.diffuse_map = window.load_texture_2d('data/base_grass5.png')
        self.diffuse_map.build_mipmaps()
        self.normal_map = window.load_texture_2d('data/base_grass5n.png')
        self.normal_map.build_mipmaps()
        self.vbo = window.ctx.buffer(
            array(
                'f',
                [
                    # Triangle strip creating a plane
                    # x, y, z, u, v
                    -150, 0, -300, 0, 0,      # lower left
                    -150, 0, 0, 0, 1,    # upper left
                    150, 0, -300, 1, 0,      # lower right
                    150, 0, 0, 1, 1     # upper right
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
        self.program['light_pos'].value = window.light_pos
        self.program['image'].value = DIFFUSE_MAP_UNIT
        self.program['normals'].value = NORMAL_MAP_UNIT
        self.program['uv_scale'].value = 3

    def draw(self, projection_matrix=None, camera_matrix=None):
        self.program["m_proj"].write(projection_matrix)
        self.program["m_cam"].write(camera_matrix)
        self.diffuse_map.use(location=DIFFUSE_MAP_UNIT)
        self.normal_map.use(location=NORMAL_MAP_UNIT)
        self.vao.render(moderngl.TRIANGLE_STRIP)
