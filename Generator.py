#!/usr/bin/env -S  python  #
# -*- coding: utf-8 -*-
# LICENSE INFORMATION HERE
"""
GENERAL DOCUMENTATION HERE
"""
import argparse
import requests
import secrets

if __name__ == '__main__':   # (if this was a package rather than a single-file module, we would just cut>
    import ast, argparse

    def OneOrTwoNumbers( s ): # custom argument "type"
        seq = ast.literal_eval( s.strip( ' [](),' ) + ',' )
        try: x, = seq
        except: x = a, b = seq

        return x

    def TwoNumbers( s ):
        seq = ast.literal_eval( s )
        x = a, b = [ float(element) for element in seq ] # will throw an exception if there aren'>

        return x

    class HelpFormatter( argparse.RawDescriptionHelpFormatter ): pass
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--number',help='the desired number of passwords to generate', default=1)
    parser.add_argument('-w','--words',help='the number of word for the password',default=4)
    parser.add_argument('-s','--size',help='the size of the words',default=None)
    parser.add_argument('-c','--chars',help='number of special characters',default=1)
    parser.add_argument('-i','--integers',help='the number of integers to add',default=1)
    parser.add_argument('-d','--digits',help='the number of digits for the integers',default=3)
    parser.add_argument('--caps',help='whether to capitalize the first letter of each word',default=False)

    args = parser.parse_args()

import numpy as np # pip install numpy

__all__ = [ # symbols listed here will be the ones the user gets when they `import *` from here
	'EndUserError',
	'PassSentence',
]

class EndUserError( Exception ): pass

class PassSentence:
    def __init__(self,
                 number_words=4,
                 word_size=None,
                 number_chars=1,
                 number_integers=1,
                 number_digit=3,
                 caps = False):

        self.number_words = number_words
        self.word_size = word_size
        self.number_chars = number_chars
        self.number_integers = number_integers
        self.number_digit = number_digit
        self.rng = np.random.default_rng()
        self.caps = caps

        if self.number_integers > self.number_words:
            self.number_integers = self.number_words

        if self.number_chars > self.number_words:
            self.number_chars = self.number_words

        self.__generate_words()
        self.__generate_chars()
        self.__generate_integers()

    def __generate_words(self):
        if self.word_size:
            response = requests.get(
                f'https://random-word-api.herokuapp.com/word?number={self.number_words}length={self.word_size}')
        else:
            response = requests.get(f'https://random-word-api.herokuapp.com/word?number={self.number_words}')

        self.__words = response.json()

        if self.caps:
            self.__words = [word.capitalize() for word in self.__words]

        return self

    def __generate_chars(self):
        ascii_values = np.concatenate([
            np.linspace(33, 47, 48 - 33),
            np.linspace(58, 64, 65 - 58),
            np.linspace(91, 96, 97 - 91),
            np.linspace(123, 126, 127 - 123)
        ])

        self.__special_chars = [chr(int(secrets.choice(ascii_values)))
                              for _ in range(self.number_chars)]

        return self

    def __generate_integers(self):
        __high_val = int('9' * self.number_digit)
        self.__integers = [secrets.randbelow(__high_val)
                         for _ in range(self.number_integers)]

        return self

    def generate_passphrase(self):
        __modified_words = self.__words.copy()

        integers_positions = [secrets.randbelow(self.number_words)
                              for _ in range(self.number_integers)]
        chars_positions = [secrets.randbelow(self.number_words)
                           for _ in range(self.number_chars)]

        for var_pos,var_var in zip([integers_positions, chars_positions],
                                   [self.__integers, self.__special_chars]):

            for i,pos in enumerate(var_pos):
                pos_in_word = secrets.randbits(1)

                if pos_in_word == 0:
                    __first = str(var_var[i])
                    __second = __modified_words[pos]

                else:
                    __first = __modified_words[pos]
                    __second = str(var_var[i])

                __modified_words[pos] = ''.join([__first, __second])

        self.passphrase = '_'.join(__modified_words)

        return self

    def shuffle_passphrase(self):
        self.rng.shuffle(self.__words)
        self.generate_passphrase()
