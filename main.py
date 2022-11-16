import moderngl
import moderngl_window as mglw
from moderngl_window.scene import KeyboardCamera
from moderngl_window import screenshot
from pathlib import Path


from grass import Grass
from terrain import Terrain


FOV = 45.0
FAR = 1000.0
NEAR = 0.1


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (1280, 720)
    resource_dir = Path(__file__).parent

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.camera_enabled = True
        self.camera = KeyboardCamera(
            self.wnd.keys,
            fov=FOV, aspect_ratio=self.wnd.aspect_ratio, near=NEAR, far=FAR
        )
        self.camera.set_position(0.0, 2.0, 0.0)
        self.camera.velocity = 25.0
        self._light_pos = (0.0, 200.0, -150.0)
        self.terrain = Terrain(self)
        self.grass = Grass(self)

    @property
    def light_pos(self) -> tuple[float, float, float]:
        return self._light_pos

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()
            if key == keys.R:
                screenshot.create(self.wnd.fbo, name='docs/screenshot.png')

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

    def render(self, time, _):
        # This method is called every frame
        self.ctx.clear(135.0 / 256.0, 206.0 / 256.0, 235.0 / 256.0)
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.BLEND)
        self.terrain.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix
        )
        self.grass.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=self.camera.matrix,
            time=time
        )


if __name__ == '__main__':
    Window.run()
