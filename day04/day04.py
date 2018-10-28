"""
--- Day 4: High-Entropy Passphrases ---

A new system policy has been put in place that requires all accounts to use a passphrase instead of simply a password.
A passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

    aa bb cc dd ee is valid.
    aa bb cc dd aa is not valid - the word aa appears more than once.
    aa bb cc dd aaa is valid - aa and aaa count as different words.

The system's full passphrase list is available as your puzzle input. How many passphrases are valid?

--- Part Two ---

For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two words
that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged to form
any other word in the passphrase.

For example:

    abcde fghij is a valid passphrase.
    abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
    a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
    iiii oiii ooii oooi oooo is valid.
    oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.

Under this new system policy, how many passphrases are valid?

"""

from collections import defaultdict


class PassValidator(object):
    def __init__(self, filename=None):
        self.file = filename

    def _has_no_repeated_words(self, passphrase):
        words = self._line_to_pass_words(passphrase)

        return len(set(words)) == len(words)

    def _has_no_anagrams(self, passphrase):
        words = self._line_to_pass_words(passphrase)
        for word_group in self._group_by_length(words).values():
            sorted_words = [''.join(sorted(word)) for word in word_group]

            if len(set(sorted_words)) != len(sorted_words):
                return False

        return True

    def _group_by_length(self, words):
        groups = defaultdict(list)
        for word in words:
            groups[len(word)].append(word)

        return groups

    def _line_to_pass_words(self, line):
        return line.strip().split()

    def count_valid(self):
        count_of_valid = 0
        if self.file is not None:
            with open(self.file, 'r', encoding='utf-8') as fh:
                for line in fh:
                    if self._has_no_repeated_words(line):
                        count_of_valid += 1

        return count_of_valid

    def count_valid_2(self):
        count_of_valid = 0
        if self.file is not None:
            with open(self.file, 'r', encoding='utf-8') as fh:
                for line in fh:
                    if self._has_no_repeated_words(line) and self._has_no_anagrams(line):
                        count_of_valid += 1

        return count_of_valid


if __name__ == '__main__':
    validator = PassValidator('day04_input.txt')
    count_of_valid_passphrases = validator.count_valid()
    print(count_of_valid_passphrases)  # 386
    count_of_valid_passphrases = validator.count_valid_2()
    print(count_of_valid_passphrases)  # 208
