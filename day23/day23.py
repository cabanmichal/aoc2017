"""
--- Day 23: Coprocessor Conflagration ---

You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental
coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause serious
issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality
seems very similar, but some of the instructions are different:

    set X Y sets register X to the value of Y.
    sub X Y decreases register X by the value of Y.
    mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
    jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the
    next instruction, an offset of -1 jumps to the previous instruction, and so on.)

    Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any
meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?

--- Part Two ---

Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1
when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient
implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer
working.

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes.
Technically, if it had that... it wouldn't even need to run the program.

After setting register a to 1, if the program were to run to completion, what value would be left in register h?

"""


class Coprocessor(object):
    def __init__(self):
        self.current_instruction_index = 0
        self.number_of_mul_invocations = 0
        self.registers = {}

        self.instruction_set = {
            'set': self._set,
            'sub': self._sub,
            'mul': self._mul,
            'jnz': self._jnz,
        }

        self._init()

    def _init(self):
        self.current_instruction_index = 0
        self.number_of_mul_invocations = 0
        self.registers = {chr(k): 0 for k in range(ord('a'), ord('h') + 1)}

    def _set(self, x, y):
        v = self.registers.get(y, y)
        self.registers[x] = v

    def _sub(self, x, y):
        v = self.registers.get(y, y)
        self.registers[x] -= v

    def _mul(self, x, y):
        v = self.registers.get(y, y)
        self.registers[x] *= v
        self.number_of_mul_invocations += 1

    def _jnz(self, x, y):
        vx = self.registers.get(x, x)
        vy = self.registers.get(y, y)

        if vx != 0:
            self.current_instruction_index += vy - 1

    @staticmethod
    def parse_instructions(filename):
        instructions = []
        with open(filename, 'r', encoding='utf-8') as fh:
            for line in fh:
                parts = line.strip().split()
                if parts:
                    for i in (1, 2):
                        try:
                            parts[i] = int(parts[i])
                        except (ValueError, IndexError):
                            continue

                    instructions.append(parts)

        return instructions

    def process(self, instructions_file, initial_config=None):
        self._init()
        instructions = self.parse_instructions(instructions_file)
        if initial_config is not None:
            self.registers.update(initial_config)

        while True:
            try:
                next_instruction = instructions[self.current_instruction_index]
                f = next_instruction[0]
                args = next_instruction[1:]
                self.instruction_set[f](*args)

                self.current_instruction_index += 1

            except IndexError:
                break

        return self.number_of_mul_invocations, self.registers.get('h')


if __name__ == '__main__':
    c = Coprocessor()
    print(c.process('day23_input.txt'))  # 8281
    # print(c.process('day23_input.txt', {'a': 1}))  # not 0
