import pathlib

import pyglet


class Cube:

    TextureCoords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))

    @staticmethod
    def load_texture(file):
        image = pyglet.image.load(file)
        # configure Texture as 2D
        pyglet.gl.glTexParameterf(
            pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER,
            pyglet.gl.GL_NEAREST
        )
        pyglet.gl.glTexParameterf(
            pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER,
            pyglet.gl.GL_NEAREST
        )
        return pyglet.graphics.TextureGroup(image.get_texture())

    def __init__(self, x, y, z, texture: [str, pathlib.Path]):
        self.texture = self.load_texture(texture)
        self.batch = pyglet.graphics.Batch()

        # coordinates start in the corner furthest away
        left = (x, y, z, x, y, z + 1, x, y + 1, z + 1, x, y + 1, z)
        right = (x + 1, y, z, x + 1, y, z + 1, x + 1, y + 1, z + 1, x + 1, y + 1, z)
        # coordinates start in the bottom left corner
        back = (x, y, z, x + 1, y, z, x + 1, y + 1, z, x, y + 1, z)
        front = (x, y, z + 1, x + 1, y, z + 1, x + 1, y + 1, z + 1, x, y + 1, z + 1)
        # coordinates start in the back left corner
        bottom = (x, y, z, x + 1, y, z, x + 1, y, z + 1, x, y, z + 1)
        top = (x, y + 1, z, x + 1, y + 1, z, x + 1, y + 1, z + 1, x, y + 1, z + 1)

        sides = [left, right, back, front, bottom, top]
        for coordinates in sides:
            self.batch.add(
                4, pyglet.gl.GL_QUADS, self.texture,
                ('v3f', coordinates),
                Cube.TextureCoords
            )

    def draw(self):
        self.batch.draw()
