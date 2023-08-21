#!/usr/bin/env -S  python  #
# -*- coding: utf-8 -*-
# LICENSE INFORMATION HERE
"""
GENERAL DOCUMENTATION HERE
"""
import os
import platform
from pathlib import Path
import sys
import datetime
import json
from cryptography.fernet import Fernet

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


from Generator import PassSentence
import keyring # https://pypi.org/project/keyring/ pip install keyring
import zxcvbn # https://pypi.org/project/zxcvbn-python/ pip install zxcvbn-python
import numpy as np # pip install numpy

__all__ = [ # symbols listed here will be the ones the user gets when they `import *` from here
	'EndUserError',
    'PasswordManager'
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
    elif default == "Yes":
        prompt = " [Yes]/No"
    elif default == "No":
        prompt = " Yes/[No] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'Yes' or 'No'.\n")

class PasswordManager:

    def __init__(self,encryption_key=None):
        self.keyring = keyring
        self.encryption_key = encryption_key

    def read_key(filename=None):
        
        pass
    def create_key(self):
        question = "You are about to generate a Fernet key to encrypt the file where all the passwords are stored. If you loose that key you won't be able to retrieve your passwords. Make sure you are saving it somewhere safe. Are you sure you want to continue?"
        query = query_yes_no(question, default="No")
        if query and not self.encryption_key:
            self.encryption_key= Fernet.generate_key()
            question="Do you want to show the key?"
            query = query_yes_no(question, default="No")
            if query: print(self.encryption_key)
            question="Do you want to save the key to a file?"
            query = query_yes_no(question, default="No")
            self.key_filename = input("Enter the filename:")
            self.key_description = input("Enter a description:")
            self.generation_date = str(datetime.datetime.now())
            if query: self.save_key()

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
                          doprint=False):

        pass_sentence = PassSentence(number_words=number_words,
                                     word_size=word_size,
                                     number_chars=number_chars,
                                     number_integers=number_integers,
                                     number_digit=number_digit,
                                     caps = caps)

        pass_sentence.generate_passphrase()
        if doprint:
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

        self._password = pass_sentence.passphrase

        return self

    def test_password(self):
        self.stats = zxcvbn.zxcvbn(self._password)
        print('CALCULATED CRACKING TIMES:')
        for key, value in self.stats['crack_times_display'].items():
            print(key.replace('_',' ')+':', value)
        print('PASSWORD STRENGTH (0-4):', self.stats['score'])
        if self.stats['feedback']['warning'] != '':
            print('WARNINGS:', self.stats['feedback']['warning'])
            print('SUGGESTIONS:', self.stats['feedback']['suggestions'])

        return self

    def enable_encryption(self):
        if not self.encryption_key:
            EndUserError('You need to create an encryption key or manually enter an existingo one')
        self.fernet = Fernet(self.encryption_key)

        return self

    def set_password(self, service, username, password=None):

        if hasattr(self,'_password') and not password:
            keyring.set_password(service, username, self._password)
            print(f'Password Stored.\n Service: {service}\n Username: {username}')

        elif not hasattr(self,'_password') and password:
            keyring.set_password(service, username, password)
            print(f'Password Stored.\n Service: {service}\n Username: {username}')

        elif not hasattr(self,'_password') and not password:
            question = "You don't have a password generated. Do you want to generate one?"
            query = query_yes_no(question, default="No")

            if query:
                print('Generating Password:')
                self.generate_password()
                print(f'Password Generated.\n Service: {service}\n Username: {username}')
                keyring.set_password(service, username, self._password)
                print(f'Password Stored')
        self.credentials= dict(
            date = str(datetime.datetime.now()),
            service=service,
            username=username,
            password=str(self.fernet.encrypt(self._password.encode('utf-8')))
        )

        return self

    def get_password(self, service, username, display = False):
        self._password = keyring.get_password(
            service,
            username
        )
        if display:
            print(f'Service: {service}\n Username: {username}')
            print(f'Password: {self._password}')

        self.credentials = dict(
            date = str(datetime.datetime.now()),
            service=service,
            username=username,
            password=str(self.fernet.encrypt(self._password.encode('utf-8')))
        )

        return self

    def export_to_json(self):
        saving_filename = os.path.join(str(Path.home()),'passwords.json')
        self.credentials.update(
            dict(
                data_file_modified = str(datetime.datetime.now()),
                associated_key_date = self.generation_date,
                associated_key_description = self.key_description,
                )
            )
        with open(saving_filename, 'a') as f:
            json.dump(self.credentials, f)
            f.write('\n')

    def save_key(self):
        saving_filename = os.path.join(
            str(Path.home()),f'{self.key_filename}.json')

        with open(f'{saving_filename}', 'a') as f:
            data = dict(
                key_generation_date = self.generation_date,
                date_file_modified= str(datetime.datetime.now()),
                description = self.key_description,
                method = 'Fernet',
                key = str(self.encryption_key)
            )
            json.dump(data, f)
            f.write('\n')
# TODO: Add a function to read the key from a file
