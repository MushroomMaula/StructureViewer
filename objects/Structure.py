import logging
import os
import pathlib
import sys
from typing import Union

import pyglet
from nbt import nbt

from Parser import StructureParser
from utils import get_latest_jar, extract_textures

ERROR_IMG = pathlib.Path(__file__).parent.parent / 'error.png'
LOGGER = logging.getLogger(__name__)

stdout = logging.StreamHandler(sys.stdout)

LOGGER.addHandler(stdout)
LOGGER.setLevel(logging.DEBUG)


class Structure:

    parser = StructureParser
    Block = pyglet.gl.GL_QUADS
    TextureCoords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

    @staticmethod
    def load_texture(name: str) -> pyglet.graphics.TextureGroup:
        """

        :param str name: Name of the texture (minecraft:name)
        :return: `pyglet.graphics.TextureGroup`
        """
        if not os.path.isdir('../textures'):
            jar = get_latest_jar()
            extract_textures(jar)
        name = name.split(':')[1]
        # TODO: add support for stairs and other 3D models
        if 'stair' in name:
            name = f'{name.split("_")[0]}_planks'
        try:
            image = pyglet.image.load(f'../textures/block/{name}.png')
        except FileNotFoundError:
            LOGGER.warning(f'Texture for <{name}> not found')
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
        x, y, z = block.pos
        texture = Structure.load_texture(block.texture.name)

        ##### coordinates of the block faces #####
        # remember z-axis in OpenGL is the y-axis in normal 3D coordinate system

        # coordinates start in the corner furthest away
        left = (x, y, z, x, y, z+1, x, y+1, z+1, x, y+1, z)
        right = (x+1, y, z, x+1, y, z+1, x+1, y+1, z+1, x+1, y+1, z)
        # coordinates start in the bottom left corner
        back = (x, y, z, x+1, y, z, x+1, y+1, z, x, y+1, z)
        front = (x, y, z+1, x+1, y, z+1, x+1, y+1, z+1, x, y+1, z+1)
        # coordinates start in the back left corner
        bottom = (x, y, z, x+1, y, z, x+1, y, z+1, x, y, z+1)
        top = (x, y+1, z, x+1, y+1, z, x+1, y+1, z+1, x, y+1, z+1)

        sides = [left, right, back, front, bottom, top]
        for coordinates in sides:
            self.batch.add(
                4, Structure.Block, texture,
                ('v3f', coordinates),
                Structure.TextureCoords
            )

    def draw(self):
        self.batch.draw()


if __name__ == '__main__':
    Structure('../with_mast_degraded.nbt')
