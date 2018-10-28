"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0,
b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

    Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise.
    (For example, s3 on abcde produces cdeab).
    Exchange, written xA/B, makes the programs at positions A and B swap places.
    Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do the following dance:

    s1, a spin of size 1: eabcd.
    x3/4, swapping the last two programs: eabdc.
    pe/b, swapping programs e and b: baedc.

After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs
standing after their dance?

--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including
the first dance, a total of one billion (1000000000) times.

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

    s1, a spin of size 1: cbaed.
    x3/4, swapping the last two programs: cbade.
    pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?

"""


class ProgramShuffler(object):
    def __init__(self, input_file):
        self._input_file = input_file
        self._programs = []
        self._processor_mapping = {'s': self._s_processor,
                                   'x': self._x_processor,
                                   'p': self._p_processor}
        self._init()

    def _init(self):
        self._programs = [chr(i) for i in range(ord('a'), ord('a') + 16)]

    def _instructions_generator(self):
        with open(self._input_file, 'r', encoding='utf-8') as fh:
            for instruction in next(fh).strip().split(','):
                yield instruction

    def _s_processor(self, *args):
        n = int(args[0])
        e = len(self._programs) - n

        self._programs = self._programs[e:] + self._programs[:e]

    def _x_processor(self, *args):
        a, b = map(int, args)
        self._programs[a], self._programs[b] = self._programs[b], self._programs[a]

    def _p_processor(self, *args):
        a, b = args
        a_idx = self._programs.index(a)
        b_idx = self._programs.index(b)

        self._programs[a_idx], self._programs[b_idx] = self._programs[b_idx], self._programs[a_idx]

    def _instructions_processor(self, raw_instruction):
        instruction, args = raw_instruction[0], raw_instruction[1:].split('/')
        self._processor_mapping[instruction](*args)

        # print('{:<6}:\t{}'.format(raw_instruction, ''.join(self._programs)))

    def shuffle(self, n=1):

        def _shuffle():
            for instruction in self._instructions_generator():
                self._instructions_processor(instruction)

            return ''.join(self._programs)

        self._init()
        shuffled = set()
        period = None

        for i in range(n):
            p_string = _shuffle()
            if p_string in shuffled:
                period = i
                break
            else:
                shuffled.add(p_string)

        if period is not None:
            self.shuffle(n % period)

        return ''.join(self._programs)


if __name__ == '__main__':
    shuffler = ProgramShuffler('day16_input.txt')
    result = shuffler.shuffle()
    print(result)  # bijankplfgmeodhc
    result = shuffler.shuffle(1000000000)
    print(result)  # bpjahknliomefdgc
