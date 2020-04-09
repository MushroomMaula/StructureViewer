import os
import pathlib
from typing import Union

import pyglet

from utils import get_latest_jar, extract_textures
from utils.classes import Block, Model

ERROR_IMG = pathlib.Path(__file__).parent.parent / 'static/error.png'


class Cube:
    TextureCoords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))

    @staticmethod
    def load_texture(fp: Union[str, pathlib.Path]) -> pyglet.graphics.TextureGroup:

        if not os.path.isdir('textures'):
            jar = get_latest_jar()
            extract_textures(jar)

        try:
            image = pyglet.image.load(f'textures/{fp}.png')
        except FileNotFoundError:
            image = pyglet.image.load(ERROR_IMG)

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

    def __init__(self, name="spruce_log"):
        self.block = Block(0, 0, 0, 1)
        self.block.model = Model.from_name(name)

        self.batch = pyglet.graphics.Batch()

        for texture, vertices in self.block.get_faces():
            self.batch.add(
                4, pyglet.gl.GL_QUADS,
                self.load_texture(texture),
                ('v3f', vertices),
                Cube.TextureCoords
            )

    def draw(self):
        self.batch.draw()


if __name__ == '__main__':
    Cube()
