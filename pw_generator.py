import numpy as np
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n','--number',help='the desired number of passwords to generate', default=1)
parser.add_argument('-w','--words',help='the number of word for the password',default=4)
parser.add_argument('-c','--chars',help='number of special characters',default=1)
parser.add_argument('-i','--integers',help='the number of integers to add',default=1)

args = parser.parse_args()


class PassSentence:
    def __init__(self,
                 number_words=4,
                 number_chars=1,
                 number_integers=1,
                 number_digit=3):

        self.number_words = number_words
        self.number_chars = number_chars
        self.number_integers = number_integers
        self.number_digit = number_digit
        self.rng = np.random.default_rng()

        if self.number_integers > self.number_words:
            self.number_integers = self.number_words

        if self.number_chars > self.number_words:
            self.number_chars = self.number_words

    def _generate_words(self):
        response = requests.get(f'https://random-word-api.herokuapp.com/word?number={self.number_words}')
        self.words = response.json()

        return self

    def _generate_chars(self):
        ascii_values = np.concatenate([
            np.linspace(33, 47, 48 - 33),
            np.linspace(58, 64, 65 - 58),
            np.linspace(91, 96, 97 - 91),
            np.linspace(123, 126, 124 - 126)
        ])

        ascii_index = self.rng.integers(low=0,
                                        high=len(ascii_values),
                                        size=self.number_chars)
        self.special_chars = [chr(val) for val in ascii_index]

        return self

    def _generate_integers(self):
        self.integers = self.rng.integers(low=0,
                                     high=self.number_digit,
                                     size=self.number_integers)

        return self

    def generate_passphrase(self):
        integers_positions = self.rng.choice(self.number_words,
                                            size=self.number_integers,
                                            replace=False)

        chars_positions = self.rng.choice(self.number_words,
                                            size=self.number_chars,
                                            replace=False)

        for i,integer in enumerate(integers_positions):

            pos_in_word = self.rng.integers(low=0,high=1,size=1)[0]

            if pos_in_word == 0:
                first = ''.join([str(self.integers),















for i in range(args.number):
