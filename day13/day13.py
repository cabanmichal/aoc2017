"""
--- Day 13: Packet Scanners ---

You need to cross a vast firewall. The firewall consists of several layers, each with a security scanner that moves
back and forth across the layer. To succeed, you must not be detected by a scanner.

By studying the firewall briefly, you are able to record (in your puzzle input) the depth of each layer and the range
of the scanning area for the scanner within it, written as depth: range. Each layer has a thickness of exactly 1.
A layer at depth 0 begins immediately inside the firewall; a layer at depth 1 would start immediately after that.

For example, suppose you've recorded the following:

0: 3
1: 2
4: 4
6: 4

This means that there is a layer immediately inside the firewall (with range 3), a second layer immediately after that
(with range 2), a third layer which begins at depth 4 (with range 4), and a fourth layer which begins at depth 6 (also
with range 4). Visually, it might look like this:

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Within each layer, a security scanner moves back and forth within its range. Each security scanner starts at the top
and moves down until it reaches the bottom, then moves up until it reaches the top, and repeats. A security scanner
takes one picosecond to move one step. Drawing scanners as S, the first few picoseconds look like this:


Picosecond 0:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 1:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

Your plan is to hitch a ride on a packet about to move through the firewall. The packet will travel along the top of
each layer, and it moves at one layer per picosecond. Each picosecond, the packet moves one layer forward (its first
move takes it into layer 0), and then the scanners move one step. If there is a scanner at the top of the layer as your
packet enters it, you are caught. (If a scanner moves into the top of its layer while you are there, you are not caught:
it doesn't have time to notice you before you leave.) If you were to do this in the configuration above, marking your
current position with parentheses, your passage through the firewall would look like this:

Initial state:
 0   1   2   3   4   5   6
[S] [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

Picosecond 0:
 0   1   2   3   4   5   6
(S) [S] ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 1:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] (S) ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 2:
 0   1   2   3   4   5   6
[ ] [S] (.) ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 3:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 4:
 0   1   2   3   4   5   6
[S] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 5:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... ... [S] (.) [S]
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]


Picosecond 6:
 0   1   2   3   4   5   6
[ ] [S] ... ... [S] ... (S)
[ ] [ ]         [ ]     [ ]
[S]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

In this situation, you are caught in layers 0 and 6, because your packet entered the layer when its scanner was at
the top when you entered it. You are not caught in layer 1, since the scanner moved into the top of the layer once
you were already there.

The severity of getting caught on a layer is equal to its depth multiplied by its range. (Ignore layers in which you do
not get caught.) The severity of the whole trip is the sum of these values. In the example above, the trip severity is
0*3 + 6*4 = 24.

Given the details of the firewall you've recorded, if you leave immediately, what is the severity of your whole trip?

--- Part Two ---

Now, you need to pass through the firewall without being caught - easier said than done.

You can't control the speed of the packet, but you can delay it any number of picoseconds. For each picosecond you
delay the packet before beginning your trip, all security scanners move one step. You're not in the firewall during
this time; you don't enter layer 0 until you stop delaying the packet.

In the example above, if you delay 10 picoseconds (picoseconds 0 - 9), you won't get caught:

State after delaying:
 0   1   2   3   4   5   6
[ ] [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

Picosecond 10:
 0   1   2   3   4   5   6
( ) [S] ... ... [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
( ) [ ] ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 11:
 0   1   2   3   4   5   6
[ ] ( ) ... ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[S] (S) ... ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 12:
 0   1   2   3   4   5   6
[S] [S] (.) ... [S] ... [S]
[ ] [ ]         [ ]     [ ]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] (.) ... [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]


Picosecond 13:
 0   1   2   3   4   5   6
[ ] [ ] ... (.) [ ] ... [ ]
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [S] ... (.) [ ] ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]


Picosecond 14:
 0   1   2   3   4   5   6
[ ] [S] ... ... ( ) ... [ ]
[ ] [ ]         [ ]     [ ]
[S]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... ( ) ... [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]


Picosecond 15:
 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] (.) [ ]
[S] [S]         [ ]     [ ]
[ ]             [ ]     [ ]
                [S]     [S]

 0   1   2   3   4   5   6
[S] [S] ... ... [ ] (.) [ ]
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]


Picosecond 16:
 0   1   2   3   4   5   6
[S] [S] ... ... [ ] ... ( )
[ ] [ ]         [ ]     [ ]
[ ]             [S]     [S]
                [ ]     [ ]

 0   1   2   3   4   5   6
[ ] [ ] ... ... [ ] ... ( )
[S] [S]         [S]     [S]
[ ]             [ ]     [ ]
                [ ]     [ ]

Because all smaller delays would get you caught, the fewest number of picoseconds you would need to delay to get
through safely is 10.

What is the fewest number of picoseconds that you need to delay the packet to pass through the firewall without being
caught?

"""

import re


class FirewallLayer(object):
    def __init__(self,  depth, scanner_position=0):
        self.depth = depth
        self.scanner_position = 0
        self._forward_direction = True

    def move_scanner(self):
        if self.depth > 1:
            if self._forward_direction:
                self.scanner_position += 1
                if self.scanner_position >= self.depth:
                    self._forward_direction = False
                    self.scanner_position = self.depth - 2
            else:
                self.scanner_position -= 1
                if self.scanner_position < 0:
                    self._forward_direction = True
                    self.scanner_position = 1


class Firewall(object):
    def __init__(self, setup_file):
        self.setup_file = setup_file
        self.setup = self._setup_from_file(setup_file)
        self.packet_position = -1
        self.severity = 0
        self.moves_count = 0

    @staticmethod
    def _setup_from_file(setup_file):
        setup = []
        pattern = r'(\d+): *(\d+)'
        pattern_obj = re.compile(pattern)

        idx = 0
        with open(setup_file, 'r', encoding='utf-8') as fh:
            for line in fh:
                match = pattern_obj.search(line.strip())
                if match is not None:
                    layer = int(match.group(1))
                    depth = int(match.group(2))
                    while layer > idx:
                        setup.append(FirewallLayer(0))
                        idx += 1

                    setup.append(FirewallLayer(depth))
                    idx += 1

        return setup

    def __str__(self):
        result = ['Move {}, packet in layer {}, severity {}'.format(self.moves_count, self.packet_position,
                                                                    self.severity)]
        for i, layer in enumerate(self.setup):
            layer_string_builder = ['{}: '.format(i)]

            if layer.depth == 0:
                if layer.scanner_position == 0 and i == self.packet_position:
                    layer_string_builder.append('(.)')
                else:
                    layer_string_builder.append('...')

            else:
                start = 0
                if i == self.packet_position:
                    start = 1
                    if layer.scanner_position == 0:
                        layer_string_builder.append('(S)')
                    else:
                        layer_string_builder.append('( )')

                for j in range(start, layer.depth):
                    if j == layer.scanner_position:
                        layer_string_builder.append('[S]')
                    else:
                            layer_string_builder.append('[ ]')

            result.append(''.join(layer_string_builder))

        return '\n'.join(result) + '\n'

    def _move(self):
        self.packet_position = (self.packet_position + 1) % len(self.setup)

        # print(self.__str__())

        for i, layer in enumerate(self.setup):
            if layer.scanner_position == 0 and i == self.packet_position:
                self.severity += i * layer.depth
                break

        for i, layer in enumerate(self.setup):
            layer.move_scanner()

        # print(self.__str__())

        self.moves_count += 1

    def _reset_firewall(self):
        self.setup = self._setup_from_file(self.setup_file)
        self.packet_position = -1
        self.severity = 0
        self.moves_count = 0

    def get_delay(self):
        delay = 0

        none_at_start = False
        while not none_at_start:
            for i, layer in enumerate(self.setup):
                if self.scanner_at_start(layer, delay + i):
                    delay += 1
                    break
            else:
                none_at_start = True

        return delay

    def get_severity(self):
        for _ in self.setup:
            self._move()

        return self.severity

    @staticmethod
    def scanner_at_start(layer, at_time):
        if layer.depth == 0:
            return False

        if layer.depth == 1:
            return True

        round_trip_time = (2 * (layer.depth - 1))

        return at_time % round_trip_time == 0


if __name__ == '__main__':
    firewall = Firewall('day13_input.txt')
    print(firewall.get_severity())  # 1900
    print(firewall.get_delay())  # 3966414
