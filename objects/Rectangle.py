import pyglet
from pyglet.graphics.vertexdomain import VertexList


class Rect:

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        r, g, b = color
        self.vertex_list: VertexList = pyglet.graphics.vertex_list(4, 'v2f', 'c3B')
        self.vertex_list.vertices = self.edges
        self.vertex_list.colors = [
            r, g, b,
            r, g, b,
            r, g, b,
            r, g, b
        ]
        self.draw_mode = pyglet.gl.GL_QUADS

    @property
    def edges(self):
        """
        :return: The edges of the rectangle
        """
        return (self.x, self.y,
                self.x + self.width, self.y,
                self.x + self.width, self.y + self.height,
                self.x, self.y + self.height
                )

    def draw(self):
        self.vertex_list.draw(self.draw_mode)
