# -*- coding: utf-8 -*-


class Game:
    """Game with matrix representation:
        0 - white stone
        1 - black stone
        None - empty cell
    """
    def __init__(self, matrix=None, dimensions=None, lineup=None):
        if not matrix:
            self.matrix = [[None] * dimensions for i in range(dimensions)]
        else:
            self.matrix = matrix

        self.dimensions = dimensions
        self.lineup = lineup

    def get_cell(self, x, y):
        return self.matrix[y - 1][x - 1]

    def set_cell(self, x, y, value):
        self.matrix[y - 1][x - 1] = value

    def action(self, x, y, color):
        try:
            stone = self.get_cell(x, y)
        except IndexError:
            return False, None

        if stone is not None:
            return False, None

        self.set_cell(x, y, color)
        return True, self.status(x, y, color)

    def is_filled(self):
        for row in self.matrix:
            for stone in row:
                if stone is None:
                    return False
        return True

    def is_lineup(self, x, y, color):
        count = 0
        for obj in self.matrix[y - 1]:
            if obj == color:
                count += 1
                if count == self.lineup:
                    return True
            else:
                count = 0

        count = 0
        for i in range(self.dimensions):
            if self.matrix[i][x - 1] == color:
                count += 1
                if count == self.lineup:
                    return True
            else:
                count = 0

        return False

    def status(self, x, y, color):
        """Return 'win', 'draw', None."""
        if self.is_lineup(x, y, color):
            return 'win'

        if self.is_filled():
            return 'draw'

        return None

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
