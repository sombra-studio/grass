from array import array
import moderngl
import numpy as np
from PIL import Image

DIFFUSE_MAP_UNIT = 0
NORMAL_MAP_UNIT = 1


class Terrain:
    def __init__(self, window, size=300, max_height=20):
        """
        Object for a 3D terrain.
        Args:
            window (Window): The window that will display this terrain.
        """
        self.size = size
        self.max_height = max_height
        self.diffuse_map = window.load_texture_2d('data/base_grass5.png')
        self.diffuse_map.build_mipmaps()
        self.normal_map = window.load_texture_2d('data/base_grass5n.png')
        self.normal_map.build_mipmaps()
        # height_map_img = Image.open('data/map_00-05-37.png')
        # self.height_map = (
        #     np.asarray(height_map_img.convert('F'), dtype=np.single) / 255
        #  ) * self.max_height
        self.height_map = np.zeros([256, 256])
        self.h, self.w = self.height_map.shape
        self.vertices = self.init_vertices()
        self.indices = self.init_indices()
        ctx = window.ctx
        self.vbo = ctx.buffer(array('f', self.vertices))
        self.ibo = ctx.buffer(array('i', self.indices))
        self.program = window.load_program('shaders/terrain.glsl')
        self.vao = ctx.vertex_array(
            self.program,
            [
                (self.vbo, '3f 2f', 'in_position', 'in_uv'),
            ],
            index_buffer=self.ibo
        )
        self.window = window
        self.program['light_pos'].value = window.light_pos
        self.program['image'].value = DIFFUSE_MAP_UNIT
        self.program['normals'].value = NORMAL_MAP_UNIT
        self.program['uv_scale'].value = 3

    def init_vertices(self):
        vertices = []
        for j in range(self.h):
            for i in range(self.w):
                x = -self.size / 2 + (i / self.w) * self.size
                y = self.height_map[j, i]
                z = -(j / self.h)* self.size
                u = i / (self.w - 1)
                v = self.h - 1 - j / (self.h - 1)
                vertex = [x, y, z, u, v]
                vertices += vertex
        return vertices

    def init_indices(self):
        indices = []
        for j in range(self.h):
            for i in range(self.w):
                bottom_idx = (j + 1) * self.w + 1 + i
                top_idx = j * self.w + i
                # Maybe this could be reversed
                indices.append(bottom_idx)
                indices.append(top_idx)
            # Add last idx and next one to make an empty triangle
            last_idx = (j + 1) * self.w - 1
            if j == self.h - 1:
                next_idx = last_idx
            else:
                next_idx = last_idx + 1 + self.w
            indices.append(last_idx)
            indices.append(next_idx)
        return indices

    def draw(self, projection_matrix=None, camera_matrix=None):
        self.program["m_proj"].write(projection_matrix)
        self.program["m_cam"].write(camera_matrix)
        self.diffuse_map.use(location=DIFFUSE_MAP_UNIT)
        self.normal_map.use(location=NORMAL_MAP_UNIT)
        self.vao.render(moderngl.TRIANGLE_STRIP)
