"""
--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in
distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast,
southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest number of steps
required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

    ne,ne,ne is 3 steps away.
    ne,ne,sw,sw is 0 steps away (back where you started).
    ne,ne,s,s is 2 steps away (se,se).
    se,sw,se,sw,sw is 3 steps away (s,s,sw).

--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

"""

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
