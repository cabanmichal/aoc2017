"""
--- Day 24: Electromagnetic Moat ---

The CPU itself is a large, black building surrounded by a bottomless pit. Enormous metal tubes extend outward from
the side of the building at regular intervals and descend down into the void. There's no way to cross, but you need
to get inside.

No way, of course, other than building a bridge out of the magnetic components strewn about nearby.

Each component has two ports, one on each end. The ports come in all different types, and only matching types can be
connected. You take an inventory of the components by their port types (your puzzle input). Each port is identified
by the number of pins it uses; more pins mean a stronger connection for your bridge. A 3/7 component, for example,
has a type-3 port on one side, and a type-7 port on the other.

Your side of the pit is metallic; a perfect surface to connect a magnetic, zero-pin port. Because of this, the first
port you use must be of type 0. It doesn't matter what type of port you end with; your goal is just to make the bridge
as strong as possible.

The strength of a bridge is the sum of the port types in each component. For example, if your bridge is made of
components 0/3, 3/7, and 7/4, your bridge has a strength of 0+3 + 3+7 + 7+4 = 24.

For example, suppose you had the following components:

0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10

With them, you could make the following valid bridges:

    0/1
    0/1--10/1
    0/1--10/1--9/10
    0/2
    0/2--2/3
    0/2--2/3--3/4
    0/2--2/3--3/5
    0/2--2/2
    0/2--2/2--2/3
    0/2--2/2--2/3--3/4
    0/2--2/2--2/3--3/5

(Note how, as shown by 10/1, order of ports within a component doesn't matter. However, you may only use each port on
a component once.)

Of these bridges, the strongest one is 0/1--10/1--9/10; it has a strength of 0+1 + 1+10 + 10+9 = 31.

What is the strength of the strongest bridge you can make with the components you have available?

--- Part Two ---

The bridge you've built isn't long enough; you can't jump the rest of the way.

In the example above, there are two longest bridges:

    0/2--2/2--2/3--3/4
    0/2--2/2--2/3--3/5

Of them, the one which uses the 3/5 component is stronger; its strength is 0+2 + 2+2 + 2+3 + 3+5 = 19.

What is the strength of the longest bridge you can make? If you can make multiple bridges of the longest length,
pick the strongest one.

"""


def load_components(filename):
    """Parse the filename and return list of components"""

    components = []
    with open(filename, 'r', encoding='utf-8') as fh:
        for line in fh:
            components.append(tuple(map(int, line.strip().split('/'))))

    return components


def components_with_port(port, components):
    """Return list of components containing required port"""

    return [c for c in components if port in c]


def bridge_score(bridge):
    """Return sum of all pins in the bridge"""

    total = 0
    for c in bridge:
        total += sum(c)

    return total


def find_free_port(taken_port, component):
    """Return the port that's not connected"""

    if taken_port == component[0]:
        free_port = component[1]
    else:
        free_port = component[0]

    return free_port


def make_bridges(components, port=0, bridge=None):
    """Given the list of components, recursively construct and yield possible bridges.

    Try to yield as long bridge as possible."""

    if bridge is None:
        bridge = []

    suitable_components = components_with_port(port, components)
    if not suitable_components:
        yield bridge

    for component in suitable_components:
        components.remove(component)
        bridge.append(component)

        yield from make_bridges(components, find_free_port(port, component), bridge)

        # backtrack
        bridge.pop()
        components.append(component)


if __name__ == '__main__':
    components = load_components('day24_input.txt')

    top_score = 0
    top_length = 0
    top_score_longest = 0

    for bridge in make_bridges(components):
        score = bridge_score(bridge)
        length = len(bridge)

        top_score = max(top_score, score)

        if length > top_length:
            top_length = length
            top_score_longest = score
        elif length == top_length:
            top_score_longest = max(top_score_longest, score)

    print(top_score)  # 1859
    print(top_score_longest)  # 1799
