import os
import pathlib
from typing import Tuple, Union, Dict, Callable

from PIL import Image

SAVE_DIR = 'textures/static'


class MultiTextureFile:

    def __init__(self, fp):
        self.fp = fp
        self.img: Image = Image.open(fp)

    def create_part(self, *coords: Tuple[int, int, int, int]):
        """
        :param coords: List containing the coordinates of the regions
        """
        width = 0
        height = 0
        crops = []
        for x, y, *end in coords:
            dx = end[0] - x
            if dx != width:
                width += dx
            height += end[1] - y
            region = self.img.crop((x, y, end[0], end[1]))
            crops.append(region)

        new = Image.new('RGB', (width, height), (255, 255, 255))
        y_offset = 0
        for region in crops:
            new.paste(region, (0, y_offset))
            y_offset += region.height

        return new


class TextureGetter:
    name: str
    get_textures: Callable[..., Dict[str, Union[str, pathlib.Path]]]


class Chest(TextureGetter):

    name = 'chest'

    @staticmethod
    def get_textures():
        fp_sides = SAVE_DIR + f'/{Chest.name}_sides.png'
        fp_top = SAVE_DIR + f'/{Chest.name}_top.png'
        # create files if they dont exist
        if not os.path.exists(fp_sides) or not os.path.exists(fp_top):
            img = MultiTextureFile(r'textures/entity/chest/normal.png')

            if not os.path.exists(fp_sides):
                sides = img.create_part(
                    (14, 14, 28, 19),
                    (14, 33, 28, 43)
                )
                sides.save(fp_sides)

            if not os.path.exists(fp_top):
                top = img.create_part(
                    (14, 19, 28, 33)
                )
                top.save(fp_top)

        sides_keys = ['east', 'south', 'north', 'west']
        sides_texture = (sides_keys, fp_sides)
        top_keys = ['up', 'down']
        top_texture = (top_keys, fp_top)

        textures = {}
        for keys, fp in [sides_texture, top_texture]:
            for key in keys:
                textures[key] = str(fp)

        return textures


class Door(TextureGetter):

    @staticmethod
    def get_textures(wood) -> Dict[str, Union[str, pathlib.Path]]:
        fp = f'block/{wood}_door_bottom'
        return {'all': fp}


if __name__ == '__main__':
    import json
    with open('test.json', 'w') as f:
        data = Chest.get_textures()
        json.dump(data, f, indent=2)
