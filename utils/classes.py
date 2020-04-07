from dataclasses import dataclass
from typing import Optional, Dict, Tuple


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