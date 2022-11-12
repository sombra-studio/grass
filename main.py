import moderngl
import moderngl_window as mglw
from moderngl_window.scene import KeyboardCamera
from pathlib import Path
from pyrr import Matrix44


fov = 45.0
far = 1000.0
near = 0.1


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (1280, 720)
    resource_dir = Path(__file__).parent

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.camera_enabled = True
        # Do initialization here
        self.grass_obj = self.load_scene("data/grass.glb")
        self.camera = KeyboardCamera(
            self.wnd.keys,
            fov=fov, aspect_ratio=self.wnd.aspect_ratio, near=near, far=far
        )
        if self.grass_obj.diagonal_size > 0:
            self.camera.velocity = self.grass_obj.diagonal_size / 5.0

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

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

    def render(self, time, frametime):
        # This method is called every frame
        self.ctx.enable_only(
            moderngl.BLEND
        )

        # Move camera in on the z axis slightly by default
        translation = Matrix44.from_translation((0, 0, -1.5), dtype='f4')
        camera_matrix = self.camera.matrix * translation

        self.grass_obj.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=camera_matrix,
            time=time
        )


if __name__ == '__main__':
    Window.run()
