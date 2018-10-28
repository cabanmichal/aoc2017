"""
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and
watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources that
are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the
state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits
which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row. For
example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of flqrgnkx-0,
the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4
bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary value,
high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins with
a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used
squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all
adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own
isolated regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4
....5.6.
7.8.55.9
.88.5...
88..5..8
.8...8..
88.8.88.-->
|      |
V      V

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the
squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242
regions are present.

How many regions are present given your key string?

"""

from day10.day10 import KnotHasher


# PUZZLE_INPUT = 'flqrgnkx'
PUZZLE_INPUT = 'oundnydw'

INPUT_TEMPLATE = '{}-{}'
DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def get_bin_hash(hash_input):
    hex_hash = KnotHasher(hash_input).get_dense_hash()
    bin_hash = bin(int(hex_hash, 16))[2:].zfill(128)

    return bin_hash


def get_count_of_used_squares(hashes):
    total = 0
    for h in hashes:
        total += h.count('1')

    return total


def make_disk_grid(hashes):
    return [list(h) for h in hashes]


def find_regions(grid):
    def _get_neighbours(r, c):
        neighbours = []
        for dr, dc in DIRECTIONS:
            nr, nc = dr + r, dc + c
            if 0 <= nr < 128 and 0 <= nc < 128:
                neighbours.append((nr, nc))

        return neighbours

    def _find_region(node, region=None):
        if region is None:
            region = []

        r, c = node
        if grid[r][c] == '1' and visited_map[r][c] is False:
            visited_map[r][c] = True
            region.append((r, c))

            for neighbour in _get_neighbours(*node):
                _find_region(neighbour, region)

        return region

    visited_map = [[False for _ in range(128)] for _ in range(128)]
    regions = []

    for row in range(len(grid)):
        for column in range(len(grid[0])):
            region = _find_region((row, column))
            if region:
                regions.append(region)

    return regions


def main(puzzle_input):
    hashes = []
    for i in range(128):
        hashes.append(get_bin_hash(INPUT_TEMPLATE.format(puzzle_input, i)))

    used_squares = get_count_of_used_squares(hashes)
    grid = make_disk_grid(hashes)
    regions = find_regions(grid)

    print("Used squares: {}".format(used_squares))  # 8106
    print("Regions: {}".format(len(regions)))  # 1164


if __name__ == '__main__':
    main(PUZZLE_INPUT)

