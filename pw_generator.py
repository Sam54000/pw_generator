import numpy as np
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n','--number',help='the desired number of passwords to generate', default=1)
parser.add_argument('-w','--words',help='the number of word for the password',default=4)
parser.add_argument('-s','--size',help='the size of the words',default=None)
parser.add_argument('-c','--chars',help='number of special characters',default=1)
parser.add_argument('-i','--integers',help='the number of integers to add',default=1)
parser.add_argument('-d','--digits',help='the number of digits for the integers',default=3)

args = parser.parse_args()


class PassSentence:
    def __init__(self,
                 number_words=4,
                 word_size=None,
                 number_chars=1,
                 number_integers=1,
                 number_digit=3):

        self.number_words = number_words
        self.word_size = word_size
        self.number_chars = number_chars
        self.number_integers = number_integers
        self.number_digit = number_digit
        self.rng = np.random.default_rng()

        if self.number_integers > self.number_words:
            self.number_integers = self.number_words

        if self.number_chars > self.number_words:
            self.number_chars = self.number_words

        self._generate_words()
        self._generate_chars()
        self._generate_integers()

    def _generate_words(self):
        if self.word_size:
            response = requests.get(
                f'https://random-word-api.herokuapp.com/word?number={self.number_words}length={self.word_size}')
        else:
            response = requests.get(f'https://random-word-api.herokuapp.com/word?number={self.number_words}')

        self.words = response.json()

        return self

    def _generate_chars(self):
        ascii_values = np.concatenate([
            np.linspace(33, 47, 48 - 33),
            np.linspace(58, 64, 65 - 58),
            np.linspace(91, 96, 97 - 91),
            np.linspace(123, 126, 127 - 123)
        ])

        self.ascii_index = list(self.rng.integers(low=0,
                                           high=len(ascii_values),
                                           size=self.number_chars,
                                           dtype=int)
                          )

        self.special_chars = [chr(int(ascii_values[index]))
                              for index in self.ascii_index]

        return self

    def _generate_integers(self):
        high_val = int('9' * self.number_digit)
        self.integers = self.rng.integers(low=0,
                                     high=high_val,
                                     size=self.number_integers,
                                     dtype=int)

        return self

    def generate_passphrase(self,doprint=True):
        modified_words = self.words.copy()

        integers_positions = self.rng.choice(self.number_words,
                                            size=self.number_integers,
                                            replace=False)

        chars_positions = self.rng.choice(self.number_words,
                                            size=self.number_chars,
                                            replace=False)

        for var_pos,var_var in zip([integers_positions, chars_positions],
                                   [self.integers, self.special_chars]):

            for i,pos in enumerate(var_pos):
                pos_in_word = self.rng.integers(low=0,
                                                high=1,
                                                size=1,
                                                dtype=int)[0]

                if pos_in_word == 0:
                    first = str(var_var[i])
                    second = modified_words[pos]

                elif pos_in_word == 1:
                    first = modified_words[pos]
                    second = str(var_var[i])

                modified_words[pos] = ''.join([first, second])

        self.passphrase = '_'.join(modified_words)

        if doprint:
            print(self.passphrase)

        return self

    def shuffle_passphrase(self):
        self.rng.shuffle(self.words)
        self.generate_passphrase()


def Main():
    if args.size:
        word_size = int(args.words_size)
    else:
        word_size = None

    for _ in range(int(args.number)):
        PassSentence(number_words=int(args.words),
                     word_size=word_size,
                     number_chars=int(args.chars),
                     number_integers=int(args.integers),
                     number_digit=int(args.digits)).generate_passphrase()


if __name__ == '__main__':
    Main()

# TODO: Add password strength calculator and keychain implementation
