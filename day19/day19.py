"""
--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input),
but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take,
starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it
reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn
left or right when there's no other option. In addition, someone has left letters on the line; these also don't change
its direction, but it can use them to keep track of where it's been. For example:

     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Given this diagram, the packet needs to take the following path:

    Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to
    the first +.
    Travel right, up, and right, passing through B in the process.
    Continue down (collecting C), right, and up (collecting D).
    Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would
see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

--- Part Two ---

The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |
     |  +--+
     A  |  C
 F---|--|-E---+
     |  |  |  D
     +B-+  +--+

...the packet would go:

    6 steps down (including the first line at the top of the diagram).
    3 steps right.
    4 steps up.
    3 steps right.
    4 steps down.
    3 steps right.
    2 steps up.
    13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?

"""


import sys
from string import ascii_uppercase


DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def next_direction(position, current_direction, grid):
    opposite_direction_idx = (DIRECTIONS.index(current_direction) + 2) % len(DIRECTIONS)

    for direction in DIRECTIONS:
        if direction == DIRECTIONS[opposite_direction_idx]:
            continue

        r, c = position
        dr, dc = direction
        nr, nc = r + dr, c + dc
        try:
            if grid[nr][nc] in '|-':
                return dr, dc
        except IndexError:
            continue


def next_position(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


def input_to_grid(filename):
    grid = []
    with open(filename, 'r', encoding='utf-8') as fh:
        for line in fh:
            grid.append(list(line.replace('\n', '')))

    return grid


def find_start(grid):
    return 0, grid[0].index('|')


def char_at_position(position, grid):
    try:
        return grid[position[0]][position[1]]
    except IndexError as err:
        print(err)
        sys.exit(1)


def main():
    grid = input_to_grid('day19_input.txt')
    current_position = find_start(grid)
    current_character = char_at_position(current_position, grid)
    current_direction = (1, 0)

    letters = []
    steps = 0
    while True:
        if current_character in ascii_uppercase:
            letters.append(current_character)
        elif current_character == '+':
            current_direction = next_direction(current_position, current_direction, grid)
        elif current_character == ' ':
            break

        current_position = next_position(current_position, current_direction)
        current_character = char_at_position(current_position, grid)
        steps += 1

    print(''.join(letters), steps)


if __name__ == '__main__':
    main()  # GSXDIPWTU 16100
