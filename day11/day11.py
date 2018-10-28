MOVES = {'n': (0, -1, 1),
         'ne': (-1, 0, 1),
         'se': (-1, 1, 0),
         's': (0, 1, -1),
         'sw': (1, 0, -1),
         'nw': (1, -1, 0)}


class HexNode(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.furthest_distance = 0

    def distance(self, other=None):
        if other is None:
            x, y, z = 0, 0, 0
        else:
            x, y, z = other.coordinates()

        return (abs(self.x - x) + abs(self.y - y) + abs(self.z - z)) // 2

    def move(self, direction):
        dx, dy, dz = MOVES.get(direction)

        self.x += dx
        self.y += dy
        self.z += dz

        self.furthest_distance = max(self.furthest_distance, self.distance())

    def coordinates(self):
        return self.x, self.y, self.z


def get_steps(filename):
    with open(filename, 'r') as fh:
        steps = (s.strip() for s in fh.read().split(','))
        for step in steps:
            yield step


if __name__ == '__main__':
    child = HexNode(0, 0, 0)
    for step in get_steps('day11_input.txt'):
        child.move(step)

    print(child.distance())  # 808
    print(child.furthest_distance)  # 1556
