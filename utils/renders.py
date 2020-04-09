import operator as op
from typing import TYPE_CHECKING, List, Tuple, Dict

import numpy as np

from utils import get_odd_even

if TYPE_CHECKING:
    from .classes import Block


class ElementRenderer:
    """
    Render based on the `elements` prop of the model
    """

    @property
    def directions(self):
        """
        :return: Dictionary containing the direction vectors of the plane
        """
        return {
            # X-Z plane
            'down': ([1, 0, 0], [0, 0, 1]),
            'up': ([1, 0, 0], [0, 0, 1]),
            # Y-Z plane
            'east': ([0, 0, 1], [0, 1, 0]),
            'west': ([0, 0, 1], [0, 1, 0]),
            # X-Y plane
            'north': ([1, 0, 0], [0, 1, 0]),
            'south': ([1, 0, 0], [0, 1, 0]),
        }

    @property
    def start_change(self):
        return {
            # one higher than down
            'up': np.array([0, 1, 0]),
            # one to the right respective to east
            'west': np.array([1, 0, 0]),
            # one forward respective to north
            'south': np.array([0, 0, 1]),
        }

    def get_side_vertices(self, start: np.array, face: Tuple[str, Dict]):
        name, values = face
        # direction vectors multiplications
        r, s = get_odd_even(values.get('uv', [0, 0, 16, 16]))
        r = op.sub(*r[::-1]) * (1 / 16)  # x direction
        s = op.sub(*s[::-1]) * (1 / 16)  # z direction

        # use direction vectors to get the vertices of the plane
        u, v = np.array(self.directions[name])
        # the points have to be in this order!!
        p2 = start + r * u
        p3 = start + r*u + s*v
        p4 = start + s * v
        return np.array([start, p2, p3, p4]).flatten()

    def __call__(self, parent: "Block",  *args, **kwargs) -> List[Tuple[str, np.array]]:
        for element in parent.model.elements:

            # change start based on face
            # e.g. move start up by 1 if we are on face='up'
            dx, dy, dz = (np.array(element['to']) - np.array(element['from'])) * (1 / 16)
            start_shift = {
                # one higher than down
                'up': np.array([0, dy, 0]),
                # one to the right respective to east
                'west': np.array([dx, 0, 0]),
                # one forward respective to north
                'south': np.array([0, 0, dz]),
            }

            for face in element['faces'].items():
                face: Tuple[str, Dict]

                start = np.array(element['from']) * (1/16) + np.array(parent.pos)
                shift = start_shift.get(face[0], np.array([0, 0, 0]))
                start += shift

                vertices = self.get_side_vertices(start, face)

                # get texture (#{name}) refers to texture set on the model
                texture_name = face[1]['texture'][1:]
                face_texture = parent.model.textures[texture_name]
                yield face_texture, vertices


if __name__ == '__main__':
    from utils.classes import Model, Block
    b = Block(0, 0, 0, 3)
    b.model = Model.from_name('spruce_stairs')
    b.get_faces()
