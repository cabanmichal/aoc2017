"""
--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you
to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's
value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction
without modifying the register. The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10

These instructions would be processed as follows:

    Because a starts at 0, it is not greater than 1, and so b is not modified.
    a is increased by 1 (to 1) because b is less than 5 (it is 0).
    c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
    c is increased by -20 (to -10) because c is equal to 10.

After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth
to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?

--- Part Two ---

To be safe, the CPU also needs to know the highest value held in any register during this process so that it can
decide how much memory to allocate to these operations. For example, in the above instructions, the highest value ever
held was 10 (in register c after the third instruction was evaluated).

"""

import operator


class Processor(object):
    def __init__(self):
        self.registers = {}
        self.largest_value_ever = 0
        self.operators = {'<': operator.lt,
                          '>': operator.gt,
                          '<=': operator.le,
                          '>=': operator.ge,
                          '==': operator.eq,
                          '!=': operator.ne,
                          'dec': operator.sub,
                          'inc': operator.add}

    def _condition_true(self, condition):
        register_value = self.registers[condition[0]]
        condition_operator = self.operators[condition[1]]
        condition_value = int(condition[2])

        if condition_operator(register_value, condition_value):
            return True

        return False

    def _parse_instruction(self, instruction):
        elements = instruction.strip().split()
        register_to_update = elements[0]
        operation = elements[1]
        value = int(elements[2])
        condition = elements[4:]

        if self._condition_true(condition):
            current_register_value = self.registers[register_to_update]
            new_register_value = self.operators[operation](current_register_value, value)
            self.registers[register_to_update] = new_register_value

            self.largest_value_ever = max(self.largest_value_ever, new_register_value)

    def _init_registers(self, filename):
        with open(filename, 'r', encoding='utf-8') as fh:
            for line in fh:
                register = line.strip().split()[0]
                self.registers[register] = 0

    def process_from_file(self, filename):
        self._init_registers(filename)
        with open(filename, 'r', encoding='utf-8') as fh:
            for line in fh:
                self._parse_instruction(line)

    def get_largest_register_value(self):
        values = iter(self.registers.values())
        biggest = next(values)

        for value in values:
            biggest = max(biggest, value)

        return biggest

    def get_largest_register_value_ever(self):
        return self.largest_value_ever


if __name__ == '__main__':
    processor = Processor()
    processor.process_from_file('day08_input.txt')
    print(processor.get_largest_register_value())  # 5221
    print(processor.get_largest_register_value_ever())  # 7491
