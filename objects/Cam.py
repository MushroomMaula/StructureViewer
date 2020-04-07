import numpy as np
import pyglet

from utils.classes import Vec3, Vec2


class Player:

    def __init__(self):
        self.pos = Vec3(0.5, 1.5, 1.5)
        self.rot = Vec2(-30, 0)

    def update(self, dt, keys):
        # make the movement more significant
        s = dt * 10
        # convert to radians
        rotY = -np.deg2rad(self.rot.y)
        dx, dz = s * np.sin(rotY), s * np.cos(rotY)

        if keys.get(pyglet.window.key.W):
            self.pos.x += dx
            self.pos.z -= dz
        if keys.get(pyglet.window.key.S):
            self.pos.x -= dx
            self.pos.z += dz
        if keys.get(pyglet.window.key.A):
            self.pos.x -= dz
            self.pos.z -= dx
        if keys.get(pyglet.window.key.D):
            self.pos.x += dz
            self.pos.z += dx

        if keys[pyglet.window.key.SPACE]:
            self.pos.y += s
        if keys[pyglet.window.key.LSHIFT]:
            self.pos.y -= s

    def mouse_motion(self, dx, dy):
        dx /= 8
        dy /= 8
        self.rot.x += dy
        self.rot.y -= dx

        if self.rot.x > 90:
            self.rot.x = 90
        elif self.rot.x < -90:
            self.rot.x = -90