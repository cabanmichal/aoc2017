"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while
spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1
(the location of the only access port for this memory system) by programs that can only move up, down, left, or right.
They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

    Data from square 1 is carried 0 steps, since it's at the access port.
    Data from square 12 is carried 3 steps, such as: down, left, left.
    Data from square 23 is carried only 2 steps: up twice.
    Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your puzzle input all the way to the access
port?

--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then,
in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including
diagonals.

So, the first few squares' values are chosen as follows:

    Square 1 starts with the value 1.
    Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
    Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
    Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
    Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.

Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?

"""


import math
import sys


PUZZLE_INPUT = 361527


class MemoryDistanceFinder(object):
    def __init__(self):
        self.number = None
        self.layer = None
        self.layer_border = []
        self.number_segment = None

    def _find_layer(self):
        if self.number is not None:
            low = math.ceil(0.5 * (math.sqrt(self.number) - 1))
            high = math.floor(0.5 * (math.sqrt(self.number - 1) + 1))
            assert low == high

            self.layer = high

    def _find_layer_border(self):
        if self.layer is not None:
            layer_sum = (self.layer * (self.layer - 1)) // 2

            self.layer_border = []
            for start_diff in range(1, 9):
                border_number = self.layer * start_diff + 8 * layer_sum + 1
                self.layer_border.append(border_number)

    def _number_is_corner_number(self):
        if self.layer_border is not None and self.number is not None:
            for i in range(1, 8, 2):
                if self.layer_border[i] == self.number:
                    return True

            return False

    def _number_is_cross_number(self):
        if self.layer_border is not None and self.number is not None:
            for i in range(0, 7, 2):
                if self.layer_border[i] == self.number:
                    return True

            return False

    def find_distance(self, number):
        try:
            number = int(number)
            if number < 1:
                raise ValueError
        except ValueError:
            sys.exit("Number must be int >= 1")

        self.number = number

        if self.number == 1:
            return 0

        self._find_layer()
        self._find_layer_border()

        if self._number_is_corner_number():
            return 2 * self.layer

        if self._number_is_cross_number():
            return self.layer

        if self.layer_border[0] < self.number < self.layer_border[1]:
            return self.layer + self.number - self.layer_border[0]

        if self.layer_border[1] < self.number < self.layer_border[2]:
            return self.layer + self.layer_border[2] - self.number

        if self.layer_border[2] < self.number < self.layer_border[3]:
            return self.layer + self.number - self.layer_border[2]

        if self.layer_border[3] < self.number < self.layer_border[4]:
            return self.layer + self.layer_border[4] - self.number

        if self.layer_border[4] < self.number < self.layer_border[5]:
            return self.layer + self.number - self.layer_border[4]

        if self.layer_border[5] < self.number < self.layer_border[6]:
            return self.layer + self.layer_border[6] - self.number

        if self.layer_border[6] < self.number < self.layer_border[7]:
            return self.layer + self.number - self.layer_border[6]

        return self.layer + self.layer_border[0] - self.number


class ClosestBiggerValueFinder(object):
    moves = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    def __init__(self):
        self.current_node = (0, 0)
        self.visited_nodes = {self.current_node: 1}

        self.move_index = 0
        self.times_this_move_repeated_so_far = 0
        self.times_this_move_should_be_repeated_total = 1
        self.number_of_moves_with_this_number_of_times = 0

    def _init(self):
        self.current_node = (0, 0)
        self.visited_nodes = {self.current_node: 1}

        self.move_index = 0
        self.times_this_move_repeated_so_far = 0
        self.times_this_move_should_be_repeated_total = 1
        self.number_of_moves_with_this_number_of_times = 0

    def _get_neighbours(self, node):
        r, c = node
        return ((r + i, c + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == 0 and j == 0))

    def _calculate_value(self, node):
        current_node_value = 0
        for neighbour in self._get_neighbours(node):
            if neighbour in self.visited_nodes:
                current_node_value += self.visited_nodes[neighbour]

        return current_node_value

    def _get_node(self):
        move = __class__.moves[self.move_index]

        return self.current_node[0] + move[0], self.current_node[1] + move[1]

    def _update_after_move(self):
        self.times_this_move_repeated_so_far += 1

        if self.times_this_move_repeated_so_far == self.times_this_move_should_be_repeated_total:
            self.move_index = (self.move_index + 1) % len(__class__.moves)
            self.times_this_move_repeated_so_far = 0
            self.number_of_moves_with_this_number_of_times += 1

        if self.number_of_moves_with_this_number_of_times == 2:
            self.times_this_move_should_be_repeated_total += 1
            self.number_of_moves_with_this_number_of_times = 0

    def solve(self, target_value):
        self._init()

        current_node_value = 0
        while current_node_value < target_value:

            self.current_node = self._get_node()
            current_node_value = self._calculate_value(self.current_node)
            self.visited_nodes[self.current_node] = current_node_value

            self._update_after_move()

        return current_node_value


if __name__ == '__main__':
    mdf = MemoryDistanceFinder()
    md = mdf.find_distance(PUZZLE_INPUT)
    print(md)
    # 326

    cbvf = ClosestBiggerValueFinder()
    cbv = cbvf.solve(PUZZLE_INPUT)
    print(cbv)
    # 363010
