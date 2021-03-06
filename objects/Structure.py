import logging
import os
import pathlib
import sys
from functools import lru_cache
from typing import Union

import pyglet
from nbt import nbt

from Parser import StructureParser
from utils import get_latest_jar, extract_textures

ERROR_IMG = pathlib.Path(__file__).parent.parent / 'textures/static/error.png'
LOGGER = logging.getLogger(__name__)

stdout = logging.StreamHandler(sys.stdout)

LOGGER.addHandler(stdout)
LOGGER.setLevel(logging.DEBUG)


class Structure:

    parser = StructureParser
    Block = pyglet.gl.GL_QUADS
    TextureCoords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

    @staticmethod
    @lru_cache(32)
    def load_texture(fp: Union[str, pathlib.Path]) -> pyglet.graphics.TextureGroup:

        if not os.path.isdir('textures'):
            jar = get_latest_jar()
            extract_textures(jar)

        try:
            if not fp.endswith('.png'):
                fp = f'{fp}.png'
            image = pyglet.image.load(f'textures/{fp}')
        except FileNotFoundError:
            LOGGER.warning('Could not find ', fp)
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

    def __init__(self, fp: Union[str, pathlib.Path]):
        self.file = nbt.NBTFile(fp)
        self.data = self.parser(fp)
        self.batch = pyglet.graphics.Batch()

        for block in self.data.blocks:
            self.add_block_vertices(block)

    def add_block_vertices(self, block: Block):
        for texture, vertices in block.get_faces():
            image = self.load_texture(texture)
            self.batch.add(
                4, Structure.Block,
                image,
                ('v3f', vertices),
                Structure.TextureCoords
            )

    def draw(self):
        self.batch.draw()


if __name__ == '__main__':
    Structure('../with_mast_degraded.nbt')
