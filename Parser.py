import os
from collections import defaultdict
from typing import Dict, List

from nbt import nbt

from utils import extract_block_models, get_latest_jar
from utils.classes import Block, Texture, Model


class StructureParser:

    def __init__(self, file):
        self.nbt_data = nbt.NBTFile(file)
        # make sure model_data exists
        if not os.path.isdir('models'):
            extract_block_models(get_latest_jar())

        self.blocks_by_texture = self._get_blocks()
        self.textures = self._get_textures()
        self._set_model()  # add the textures to the blocks

    @property
    def blocks(self):
        blocks = []
        for lst in self.blocks_by_texture.values():
            blocks.extend(lst)
        return blocks

    def _get_blocks(self) -> Dict[int, List[Block]]:
        blocks = defaultdict(list)
        for b in self.nbt_data['blocks']:
            block = Block.from_nbt(b)
            blocks[block.state].append(block)
        return blocks

    def _get_textures(self) -> Dict[int, Texture]:
        block_states = {}
        palette = self.nbt_data['palettes'][0]
        for idx, state in enumerate(palette.tags):
            # the last tag is the block name
            name = state.tags.pop(-1).value
            name = name.split(':')[1]
            # grab properties
            if state.tags:
                properties = {}
                for pname, value in state.tags[0].items():
                    properties[pname] = value
            else:
                properties = None

            block_states[idx] = Texture(name, properties)
        return block_states

    def _set_model(self):
        """
        Sets the model for every block inplace
        """
        for idx, blocks in self.blocks_by_texture.items():
            # set model for every block with this texture index
            for b in blocks:
                texture = self.textures[idx]
                b.model = Model.from_name(texture.name)
