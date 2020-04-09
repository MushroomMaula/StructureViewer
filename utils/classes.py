import pathlib
from dataclasses import dataclass
from typing import Optional, Dict, Tuple, Union, List

from . import load_json
from .renders import ElementRenderer
from .textures import TextureGetter


@dataclass
class Vec2:
    x: float
    y: float


@dataclass
class Vec3(Vec2):
    z: float


@dataclass
class Texture:
    name: str
    properties: Optional[Dict[str, str]]


@dataclass
class Model:
    elements: List[Dict[str, Union[List, Dict]]]
    textures: Dict[str, Union[str, pathlib.Path]] = None

    @classmethod
    def from_name(cls, tname):
        data = Model.get_data(tname)
        # noinspection PyTypeChecker
        return cls(data['elements'], data['textures'])

    @staticmethod
    def get_data(name: str):
        fp = Model.expand_path(f'item/{name}')
        hierarchy = []
        content = load_json(fp)
        textures: Dict[str, str] = {}
        is_entity = False
        is_door = False
        # iterate over the parents until we have found the
        # last parent it should be block/block.json most of time
        while content:
            hierarchy.append(content)
            parent = content.get('parent')
            # take the texture from a entity file
            if parent == 'builtin/entity':
                # import the standard block model
                parent = "block/cube"
                # we dont use block/cube_all as we want to
                # set the textures for our faces
                is_entity = True

            elif parent == 'builtin/generated' and 'door' in name:
                # for simplicity we generate a door as a cube
                # with the same texture on all sides
                parent = "block/cube_all"
                is_door = True

            if parent:
                path = Model.expand_path(parent)
                content = load_json(path)
                # save textures for later user
                textures.update(content.get('textures', {}))
                continue
            break

        # import textures for edge cases such as doors and chests
        if is_entity:
            from . import textures as special_textures
            getter: TextureGetter = getattr(special_textures, name.title())
            textures = getter.get_textures()

        elif is_door:
            from . import textures as special_textures
            # extract the wood from the name ({wood}_door)
            getter: TextureGetter = getattr(special_textures, 'Door')
            wood = name.split('_')[0]
            textures.update(getter.get_textures(wood))

        # overwrite the values from all the parents
        # with the values from our texture (the last child)
        dct = {}
        for child in hierarchy[::-1]:
            # we already have textures from before
            child.pop('textures', None)
            dct.update(child)

        for name, texture_path in textures.items():
            # textures which start with # refer to a
            # texture_path further down the tree
            if texture_path.startswith('#'):
                # we obtain the final texture path by looking up
                # the variable in the textures
                textures[name] = textures[texture_path[1:]]
        dct['textures'] = textures
        return dct

    @staticmethod
    def expand_path(value):
        return pathlib.Path(__file__).parent.parent / f'models/{value}.json'


@dataclass
class Block(Vec3):
    state: int
    texture: Texture = None

    @property
    def pos(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    @classmethod
    def from_nbt(cls, data):
        pos = [tag.value for tag in data['pos']]
        state = data['state'].value
        return cls(*pos, state)