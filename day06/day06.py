"""
--- Day 6: Memory Reallocation ---

A debugger program here is having an issue: it is trying to repair a memory reallocation routine,
but it keeps getting stuck in an infinite loop.

In this area, there are sixteen memory banks; each memory bank can hold any number of blocks.
The goal of the reallocation routine is to balance the blocks between the memory banks.

The reallocation routine operates in cycles. In each cycle, it finds the memory bank with the most blocks
(ties won by the lowest-numbered memory bank) and redistributes those blocks among the banks. To do this,
it removes all of the blocks from the selected bank, then moves to the next (by index) memory bank and inserts
one of the blocks. It continues doing this until it runs out of blocks; if it reaches the last memory bank,
it wraps around to the first one.

The debugger would like to know how many redistributions can be done before a blocks-in-banks configuration is produced
that has been seen before.

For example, imagine a scenario with only four memory banks:

    The banks start with 0, 2, 7, and 0 blocks. The third bank has the most blocks, so it is chosen for redistribution.
    Starting with the next bank (the fourth bank) and then continuing to the first bank, the second bank, and so on,
    the 7 blocks are spread out over the memory banks. The fourth, first, and second banks get two blocks each,
    and the third bank gets one back. The final result looks like this: 2 4 1 2.
    Next, the second bank is chosen because it contains the most blocks (four). Because there are four memory banks,
    each gets one block. The result is: 3 1 2 3.
    Now, there is a tie between the first and fourth memory banks, both of which have three blocks. The first bank
    wins the tie, and its three blocks are distributed evenly over the other three banks, leaving it with none: 0 2 3 4.
    The fourth bank is chosen, and its four blocks are distributed such that each of the four banks
    receives one: 1 3 4 1.
    The third bank is chosen, and the same thing happens: 2 4 1 2.

At this point, we've reached a state we've seen before: 2 4 1 2 was already seen. The infinite loop is detected
after the fifth block redistribution cycle, and so the answer in this example is 5.

Given the initial block counts in your puzzle input, how many redistribution cycles must be completed
before a configuration is produced that has been seen before?

--- Part Two ---

Out of curiosity, the debugger would also like to know the size of the loop: starting from a state that
has already been seen, how many block redistribution cycles must be performed before that same state is seen again?

In the example above, 2 4 1 2 is seen again after four cycles, and so the answer in that example would be 4.

How many cycles are in the infinite loop that arises from the configuration in your puzzle input?

"""


class MemoryReallocator(object):
    def __init__(self, memory=None):
        if memory is None:
            self.memory = []
        else:
            self.memory = [bank for bank in memory]

        self.original_memory_state = []
        self.previous_configurations = {}
        self.redistribution_cycles_count = 0

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r', encoding='utf-8') as fh:
            first_line = next(fh)
            return __class__(map(int, first_line.strip().split('\t')))

    def __repr__(self):
        return ' '.join(map(str, self.memory))

    def _backup_memory(self):
        self.original_memory_state = [bank for bank in self.memory]

    def _restore_memory(self):
        self.memory = [bank for bank in self.original_memory_state]

    def _get_next_bank(self):
        biggest_idx = 0
        biggest_value = self.memory[biggest_idx]

        for idx, value in enumerate(self.memory):
            if value > biggest_value:
                biggest_value = value
                biggest_idx = idx

        return biggest_idx, biggest_value

    def _make_redistribution(self):
        memory_length = len(self.memory)
        biggest_bank_idx, biggest_bank_value = self._get_next_bank()

        self.memory[biggest_bank_idx] = 0
        for i in range(biggest_bank_value):
            bank_to_update_idx = (biggest_bank_idx + i + 1) % memory_length
            self.memory[bank_to_update_idx] += 1

        self.redistribution_cycles_count += 1

    def _reinit_state(self, backup=False):
        if self.original_memory_state:
            self._restore_memory()

        self.redistribution_cycles_count = 0
        self.previous_configurations = {}

        if backup:
            self._backup_memory()

    def redistribute(self, get_cycle_length=False):
        self._reinit_state(backup=True)

        memory_snapshot = tuple(self.memory)
        self.previous_configurations[memory_snapshot] = self.redistribution_cycles_count

        try:
            while True:
                self._make_redistribution()
                memory_snapshot = tuple(self.memory)
                if memory_snapshot in self.previous_configurations:
                    break

                self.previous_configurations[memory_snapshot] = self.redistribution_cycles_count

        finally:
            self._restore_memory()

        if get_cycle_length:
            first_time_seen = self.previous_configurations[memory_snapshot]
            return self.redistribution_cycles_count, self.redistribution_cycles_count - first_time_seen

        return self.redistribution_cycles_count


if __name__ == '__main__':
    mr = MemoryReallocator().from_file('day06_input.txt')
    # mr = MemoryReallocator([0, 2, 7, 0])
    print(mr.redistribute(get_cycle_length=True))  # 12841
    print(mr.redistribute(get_cycle_length=True))  # 12841
