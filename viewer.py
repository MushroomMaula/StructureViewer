import pyglet

from objects.Cam import Player
from objects.Structure import Structure
from utils.classes import Vec3, Vec2


def push(pos: Vec3, rot: Vec2):
    pyglet.gl.glPushMatrix()
    pyglet.gl.glRotatef(-rot.x, 1, 0, 0)
    pyglet.gl.glRotatef(-rot.y, 0, 1, 0)
    pyglet.gl.glTranslatef(-pos.x, -pos.y, -pos.z)


def Projection():
    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()


def Model():
    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.set_minimum_size(200, 200)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule(self.update)

        self.mouse_lock = False
        self.player = Player()
        self.model = Structure('with_mast_degraded.nbt')

    # Projections
    def set2d(self):
        Projection()
        pyglet.gl.gluOrtho2D(0, self.width, 0, self.height)
        Model()

    def set3d(self):
        Projection()
        pyglet.gl.gluPerspective(70, self.width/self.height, 0.05, 1000)
        Model()

    # Properties
    def set_mouse_lock(self):
        self.set_exclusive_mouse(not self.mouse_lock)
        self.mouse_lock = not self.mouse_lock

    # Event handling
    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_key_press(self, KEY, _):
        if KEY == pyglet.window.key.ESCAPE:
            self.close()
        elif KEY == pyglet.window.key.E:
            self.set_mouse_lock()
        self.player.update(0.001, KEY)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_lock:
            self.player.mouse_motion(dx, dy)

    def on_draw(self):
        self.clear()
        self.set3d()
        push(self.player.pos, self.player.rot)
        self.model.draw()
        pyglet.gl.glPopMatrix()


if __name__ == '__main__':
    win = Window(600, 400, resizable=True, caption='Structure Preview')
    pyglet.gl.glClearColor(0.5, 0.7, 1, 1)
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    pyglet.app.run()
