"""
--- Day 7: Recursive Circus ---
Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves
into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large
tower.

One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced several
more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs, each holding their
own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping the disc
below them balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of these towers. You ask each program to yell out
their name, their weight, and (if they're holding a disc) the names of the programs immediately above them balancing
on that disc. You write this information down (your puzzle input). Unfortunately, in their panic, they don't do this
in an orderly fashion; by the time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth
In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx, and fwft.
Those programs are, in turn, holding up other programs; in this example, none of those programs are holding up
any other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is much
larger.)

Before you're ready to help them, you need to make sure your information is correct. What is the name of the
bottom program?

--- Part Two ---
The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all
of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's fixed,
they're stuck here.

For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers
are supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum of the weights
of the programs in that tower.

In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have the same
weight, and they do: 61.

However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each match.
This means that the following sums must all be the same:

ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243
As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the nodes above ugml
are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the towers
balanced. If this change were made, its weight would be 60.

Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?

"""

import collections
import re


class Program(object):
    def __init__(self, name, weight=None, parent=None, children=None):
        self.name = name
        self.weight = weight
        self.parent = parent
        self.children = children
        if self.children is None:
            self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children


class Tower(object):
    def __init__(self):
        self.programs = {}

    def __repr__(self):
        string_builder = []
        for p in self.programs.values():
            name = p.name
            parent = p.parent
            children = p.children
            weight = p.weight

            s = "Program '{}' with parent '{}', children '{}' and weight '{}'".format(name, parent, children, weight)
            string_builder.append(s)

        return '\n'.join(sorted(string_builder))

    def add_program(self, program):
        our_program = self.programs.get(program.name)

        if our_program is not None:
            if our_program.parent is None:
                our_program.parent = program.parent

            if our_program.weight is None:
                our_program.weight = program.weight

            for child in program.get_children():
                our_program.add_child(child)

        else:
            self.programs[program.name] = program

    def add_programs_from_file(self, filename):
        pattern = r'([a-z]+) \((\d+)\)( -> (.+))?'
        pattern_obj = re.compile(pattern)

        with open(filename, 'r', encoding='utf-8') as fh:
            for line in fh:
                match = pattern_obj.search(line.strip())
                if match is not None:
                    name, weight, _, children_string = match.groups()
                    children_names = []
                    if children_string is not None:
                        children_names = children_string.split(', ')

                    self.add_program(Program(name, weight=int(weight), children=children_names))

                    for child_name in children_names:
                        self.add_program(Program(child_name, parent=name))

    def find_unbalanced_subtree(self, node):
        weights_mapping = collections.defaultdict(list)
        for child in node.get_children():
            weights_mapping[self.tree_weight(self.programs[child])].append(child)

        correct_weight = None
        incorrect_weight = None
        for weight, children in weights_mapping.items():
            if len(children) == 1:
                incorrect_weight = weight
            else:
                correct_weight = weight

        if incorrect_weight is None:
            return

        unbalanced_node = self.programs[weights_mapping[incorrect_weight][0]]

        return unbalanced_node, incorrect_weight, correct_weight

    def tree_weight(self, node):
        total_weight = 0

        node_weight = node.weight
        if node_weight is not None:
            total_weight += node_weight

        for child in node.get_children():
            total_weight += self.tree_weight(self.programs[child])

        return total_weight

    def find_correct_weight_of_unbalanced_node(self, node):
        unbalanced_subnode = self.find_unbalanced_subtree(node)

        if unbalanced_subnode is not None:
            return self.find_correct_weight_of_unbalanced_node(unbalanced_subnode[0])

        _, incorrect_weight, correct_weight = self.find_unbalanced_subtree(self.programs[node.parent])
        return correct_weight - incorrect_weight + node.weight

    def find_root(self):
        for p in self.programs.values():
            if p.parent is None:
                return p


if __name__ == '__main__':
    tower = Tower()
    # tower.add_programs_from_file('day07_input_short.txt')
    tower.add_programs_from_file('day07_input.txt')
    root = tower.find_root()
    correct_weight = tower.find_correct_weight_of_unbalanced_node(root)

    print(root.name)  # veboyvy
    print(correct_weight)  # 749
