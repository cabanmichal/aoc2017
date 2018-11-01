"""
--- Day 21: Fractal Art ---

You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail
of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always
begins with this pattern:

.#.
..#
###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

Then, the program repeats the following process:

    If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3
    square by following the corresponding enhancement rule.
    Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square
    into a 4x4 square by following the corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The artist
explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the output
pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated
by slashes. For example, the following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns
match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square;
the square matches the second rule, which produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation
to line up with the rule. The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

--- Part Two ---

How many pixels stay on after 18 iterations?

"""


def print_grid(grid):
    """Helper function to print the grid nicely formatted."""

    for row in grid:
        print('|'.join(map(str, row)))
    print()


def rotate(grid):
    """Return shallow copy of the grid rotated 90 degrees clockwise."""

    return list(map(list, zip(*reversed(grid))))


def reflect_h(grid):
    """Return shallow copy of the grid flipped around horizontal axis."""

    return list(reversed(grid))


def reflect_v(grid):
    """Return shallow copy of the grid flipped around vertical axis."""

    return list(list(reversed(row)) for row in grid)


def grid_variants(grid):
    """Yield all rotated/flipped variants of the grid."""

    n_grid = grid
    for _ in range(4):
        n_grid = rotate(n_grid)
        yield n_grid

        h_grid = reflect_h(n_grid)
        yield h_grid

        v_grid = reflect_v(n_grid)
        yield v_grid


def grid_to_string(grid):
    """Convert grid to string as in PUZZLE_INPUT and return it."""

    return '/'.join(''.join(r) for r in grid)


def string_to_grid(astring):
    """Convert grid represented as a string in PUZZLE_INPUT to list of lists and return it."""

    return [list(r) for r in astring.split('/')]


def merge_grids(grids):
    """Merge grids to one big grid and return it."""

    n = int(len(grids)**0.5)  # there must be 1, 4, 9, 16, ... grids
    h = len(grids[0])  # how many row one grid has
    grid = []
    s = 0
    for n in range(n, len(grids)+1, n):
        for i in range(h):
            r = []
            for g in grids[s:n]:
                r.extend(g[i])
            grid.append(r)
        s = n

    return grid


def split_grid(grid):
    """Split grid into square grids of equal size of either 2 or 3 rows. Yield these smaller grids one by one."""

    grid_type = None
    for n in (2, 3):
        if len(grid) % n == 0:
            grid_type = n
            break

    if grid_type is None:
        return

    s_r = 0
    for r in range(grid_type, len(grid) + 1, grid_type):
        s_c = 0
        for c in range(grid_type, len(grid[0]) + 1, grid_type):
            g = []
            for row in grid[s_r:r]:
                g.append(row[s_c:c])
            s_c = c
            yield g
        s_r = r


def count_active(grid):
    """Return number of pixels that are ON in the grid."""

    return grid_to_string(grid).count('#')


def parse_input(filename):
    """Parse input file with instructions into a dict and return it."""

    result = {}
    with open(filename, 'r', encoding='utf-8') as fh:
        for line in fh:
            k, v = line.strip().split(' => ')
            result[k] = v

    return result


def solve(initial_grid, instructions_file, iterations):
    """Solve the puzzle, return number of pixels that are ON in the final grid after given number of iterations."""

    instructions = parse_input(instructions_file)
    grid = initial_grid
    for _ in range(iterations):
        new_grids = []
        for g in split_grid(grid):
            for variant in grid_variants(g):
                new_grid = instructions.get(grid_to_string(variant))
                if new_grid is not None:
                    new_grids.append(string_to_grid(new_grid))
                    break

        grid = merge_grids(new_grids)

    return count_active(grid)


if __name__ == '__main__':
    GRID = [['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]
    PUZZLE_INPUT = 'day21_input.txt'

    print(solve(GRID, PUZZLE_INPUT, 5))  # 167
    print(solve(GRID, PUZZLE_INPUT, 18))  # 2425195
