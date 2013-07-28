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
            return False

        if stone is not None:
            return False

        self.set_cell(x, y, color)
        return True

    def is_lineuped(self, color):
        pass

    def is_filled(self):
        for row in self.matrix:
            for stone in row:
                if stone is None:
                    return False
        return True

    def is_finished(self):
        """Return tuple (is_finish, finished_status).
        If game is finished, finished_status can be:
            0 - win 0 (white)
            1 - win 1 (black)
            None - draw
        """
        if self.is_lineuped(0):
            return True, 0

        if self.is_lineuped(1):
            return True, 1

        if self.is_filled():
            return True, None

        return False, None

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
