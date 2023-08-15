import numpy as np
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n','--number',help='the desired number of passwords to generate', default=1)
parser.add_argument('-w','--words',help='the number of word for the password',default=4)
parser.add_argument('-c','--chars',help='number of special characters',default=1)
parser.add_argument('-i','--integers',help='the number of integers to add',default=1)

args = parser.parse_args()

ascii_values = np.concatenate([
    np.linspace(33, 47, 48 - 33),
    np.linspace(58, 64, 65 - 58),
    np.linspace(91, 96, 97 - 91),
    np.linspace(123, 126, 124 - 126)
])

class PassSentence:
    def __init__(self,number_words,number_chars,number_integers)
def word_generator(number = 4):
    response = requests.get(f'https://random-word-api.herokuapp.com/word?number={number}')
    words = response.json()

    return words

for i in range(args.number):
