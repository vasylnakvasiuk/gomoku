# -*- coding: utf-8 -*-


class Game:
    """Game with matrix representation:
        0 - white stone
        1 - black stone
        None - empty cell
    """
    def __init__(self, matrix=None, dimension=None, lineup=None):
        if not matrix:
            self.matrix = [[None] * dimension for i in range(dimension)]
        else:
            self.matrix = matrix

        self.dimension = dimension
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
        # Horizontal roundtrip.
        count = 0
        for obj in self.matrix[y - 1]:
            if obj == color:
                count += 1
                if count == self.lineup:
                    return True
            else:
                count = 0

        # Vertical roundtrip.
        count = 0
        for i in range(1, self.dimension + 1):
            if self.get_cell(x, i) == color:
                count += 1
                if count == self.lineup:
                    return True
            else:
                count = 0

        # Diagonal roundtrip.
        # Intersection with left side.
        x1, y1 = 1, x + y - 1
        # Intersection with downside.
        x2, y2 = x + y - self.dimension, self.dimension

        if y1 <= self.dimension:
            pos_x = x1
            pos_y = y1
        else:
            pos_x = x2
            pos_y = y2

        count = 0
        while (pos_x <= self.dimension) and (pos_y <= self.dimension):
            if self.get_cell(pos_x, pos_y) == color:
                count += 1
                if count == self.lineup:
                    return True
            else:
                count = 0

            pos_x += 1
            pos_y -= 1

        # Anti-diagonal roundtrip.
        # Intersection with left side.
        x1, y1 = 1 + (x - y), 1
        # Intersection with downside.
        x2, y2 = 1, 1 - (x - y)

        if x1 >= 1:
            pos_x = x1
            pos_y = y1
        else:
            pos_x = x2
            pos_y = y2

        count = 0
        while (pos_x <= self.dimension) and (pos_y <= self.dimension):
            if self.get_cell(pos_x, pos_y) == color:
                count += 1
                if count == self.lineup:
                    return True
            else:
                count = 0

            pos_x += 1
            pos_y += 1

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
                    result.append({
                        'x': x + 1,
                        'y': y + 1,
                        'color': 'black' if stone == 1 else 'white'
                    })
        return result
