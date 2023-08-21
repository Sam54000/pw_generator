#!/usr/bin/env -S  python  #
# -*- coding: utf-8 -*-
# LICENSE INFORMATION HERE
"""
GENERAL DOCUMENTATION HERE
"""

import os
import platform
import json
import argparse
from cryptography.fernet import Fernet
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

import keyring # https://pypi.org/project/keyring/ pip install keyring
import zxcvbn # https://pypi.org/project/zxcvbn-python/ pip install zxcvbn-python
import numpy as np # pip install numpy
from keyrings.cryptfile.cryptfile import CryptFileKeyring

if platform.system() == 'Darwin': # macOS
    from keyrings.osx_keychain import OSXKeychain
elif platform.system() == 'Linux': # Linux
    from keyrings.jeepney import Keyring
    from keyrings.alt import SecretService

__all__ = [ # symbols listed here will be the ones the user gets when they `import *` from here
	'Main',
	'EndUserError',
	'PassSentence',
	'PassWordGenerator',
]

class EndUserError( Exception ): pass

def query_yes_no(question, default=None):
    """
    Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"Yes": True, "No": False}
    if default is None:
        prompt = " [Yes/No] "
    elif default == "yes":
        prompt = " [Yes]/No"
    elif default == "no":
        prompt = " Yes/[No] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'Yes' or 'No'.\n")

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

    def _generate_chars(self):
        ascii_values = np.concatenate([
            np.linspace(33, 47, 48 - 33),
            np.linspace(58, 64, 65 - 58),
            np.linspace(91, 96, 97 - 91),
            np.linspace(123, 126, 127 - 123)
        ])

        self.special_chars = [chr(int(secrets.choice(ascii_values)))
                              for _ in range(self.number_chars)]

        return self

    def _generate_integers(self):
        high_val = int('9' * self.number_digit)
        self.integers = [secrets.randbelow(high_val)
                         for _ in range(self.number_integers)]

        return self

    def generate_passphrase(self,doprint=True):
        modified_words = self.words.copy()

        integers_positions = [secrets.randbelow(self.number_words)
                              for _ in range(self.number_integers)]
        chars_positions = [secrets.randbelow(self.number_words)
                           for _ in range(self.number_chars)]

        for var_pos,var_var in zip([integers_positions, chars_positions],
                                   [self.integers, self.special_chars]):

            for i,pos in enumerate(var_pos):
                pos_in_word = secrets.randbits(1)

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

class PasswordManager:

    def __init__(self,encryption_key=None, show_password=False):
        self.keyring = CryptFileKeyring()
        self.encryption_key = encryption_key
        self.show_password = show_password

    def create_key(self):
        question = "You are about to generate a Fernet key to encrypt the file where all the passwords are stored. If you loose that key you won't be able to retrieve your passwords. Make sure you are saving it somewhere safe. Are you sure you want to continue?"
        query = query_yes_no(question, default="No")
        if query and not self.encryption_key:
            self.encryption_key= Fernet.generate_key()
        elif query and self.encryption_key:
            raise EndUserError("You already entered an encryption key")

        return self

    def generate_password(self,
                          number_words=4,
                          word_size=None,
                          number_chars=1,
                          number_integers=1,
                          number_digit=3,
                          caps = False,
                          doprint=False)

        pass_sentence = PassSentence(number_words=number_words,
                                     word_size=word_size,
                                     number_chars=number_chars,
                                     number_integers=number_integers,
                                     number_digit=number_digit,
                                     caps = caps)

        pass_sentence.generate_passphrase()
        if doprint:
            if self.encrypt:
                print(f"Encrypted Password:{self.fernet.encrypt(pass_sentence.passphrase.encode('utf-8'))}")
            elif not self.encrypt:
                question= "You are about to display a non encrypted password. Are you sure you want to continue?"
                query = query_yes_no(question, default="No")
                if query:
                    print(f"Password:{pass_sentence.passphrase}")
                else:
                    question= "Do you want to encrypt the password?"
                    query = query_yes_no(question, default="No")
                    if query:
                        self.enable_encryption()
                        print(f"Encrypted Password:{self.fernet.encrypt(pass_sentence.passphrase.encode('utf-8'))}")

        self.password = pass_sentence.passphrase

        return self

    def test_password(self):
        self.stats = zxcvbn.zxcvbn(self.password)
        print('CALCULATED CRACKING TIMES:')
        for key, value in self.stats['crack_times_display'].items():
            print(key.replace('_',' '), value)
        print('PASSWORD STRENGTH (0-4):', self.stats['score'])
        if self.stats['feedback'] != '':
            print('WARNING:', self.stats['feedback']['warning'])
            print('SUGGESTIONS:', self.stats['feedback']['suggestions'])

        return self

    def enable_encryption(self):
        if not self.encryption_key:
            EndUserError('You need to create an encryption key or manually enter an existingo one')
        self.fernet = Fernet(self.encryption_key)
        self.encrypt = True

        return self

    def set_password(self, service, username, password=None):

        if isinstance(self.password, str) and not password:
            keyring.set_password(service, username, self.password)
            print(f'Password Stored.\n Service: {service}\n Username: {username}')

        elif not isinstance(self.password, str) and password:
            keyring.set_password(service, username, password)
            print(f'Password Stored.\n Service: {service}\n Username: {username}')

        elif not isinstance(self.password, str) and not password:
            question = "You don't have a password generated. Do you want to generate one?"
            query = query_yes_no(question, default="No")

            if query:
                print('Generating Password:')
                self.generate_password(doprint=self.show_password)
                print(f'Password Generated.\n Service: {service}\n Username: {username}')
                keyring.set_password(service, username, self.password)
                print(f'Password Stored')

    def get_password(self, service, username):
        if self.encrypt:
            password = fernet.encrypt(keyring.get_password(
                service,
                username
            ).encode('utf-8'))
        else:
        self.retrieved_password = dict(
            service=service,
            username=username,
            password=keyring.get_password(service, username)
        )

        if encrypted_password:
            return self.decrypt(encrypted_password)

        return None

    def _import_to_system_keychain_linux(self, service, username, password):
        keyring = Keyring()

        try:
            keyring.set_password(service, username, password)
            print("Password imported to Linux SecretService keyring.")
        except Exception as e:
            print("Failed to import password to Linux SecretService keyring:", e)

    def _import_to_system_keychain_macos(self, service, username, password):
        keyring = OSXKeychain()

        try:
            keyring.set_password(service, username, password)
            print("Password imported to macOS Keychain.")
        except Exception as e:
            print("Failed to import password to macOS Keychain:", e)

    def _import_to_system_keychain_windows(self, service, username, password):
        keyring = CryptFileKeyring()

        try:
            keyring.set_password(service, username, password)
            print("Password imported to Windows keyring.")
        except Exception as e:
            print("Failed to import password to Windows keyring:", e)


    def import_to_system_keychain(self, service, username, password):
        # Platform-specific code to import to system keychain

        if platform.system() == "Linux":
            self._import_to_system_keychain_linux(service, username, password)
        elif platform.system() == "Darwin":
            self._import_to_system_keychain_macos(service, username, password)
        elif platform.system() == "Windows":
            self._import_to_system_keychain_windows(service, username, password)
        else:
            print("Unsupported operating system.")

    def generate_and_store_password(self, service, username):
        # Generate passphrase
        passphrase = PassSentence(
            number_words=4,
            word_size=None,
            number_chars=1,
            number_integers=1,
            number_digit=3,
            caps = False).generate_passphrase(doprint=False)

        # Store in encrypted file
        encrypted_data = {
            "service": service,
            "username": username,
            "passphrase": encrypted_passphrase.decode('utf-8')
        }
        with open('passwords.json', 'a') as f:
            json.dump(encrypted_data, f)
            f.write('\n')
        # Store in system keyring
        self.store_password(service, username, passphrase)
        # Import to system keychain
        self.import_to_system_keychain(service, username, passphrase)


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
