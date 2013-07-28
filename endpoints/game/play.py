# -*- coding: utf-8 -*-


class Game:
    """Game with matrix representation:
        0 - white stone
        1 - black stone
        None - empty cell
    """
    def __init__(self, matrix=None, dimensions=None, lineup=None):
        if not matrix:
            self.matrix = [[None] * dimensions] * dimensions
        else:
            self.matrix = matrix

        self.dimensions = dimensions
        self.lineup = lineup

    def get_cell(self, x, y):
        return self.matrix[y - 1][x - 1]

    def set_cell(self, x, y, value):
        self.matrix[y - 1][x - 1] = value

    def action(self, x, y, color):
        color_dict = {
            'white': 0,
            'black': 1
        }
        self.set_cell(x, y, color_dict[color])
        return True

    def serialize_cells(self):
        result = []
        for y, row in enumerate(self.matrix):
            for x, stone in enumerate(row):
                if stone is not None:
                    result.append(
                        {
                            'x': x + 1,
                            'y': y + 1,
                            'color': 'black' if stone == 1 else 'white'
                        }
                    )
        return result
