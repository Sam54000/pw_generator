#!/usr/bin/env -S  python  #
# -*- coding: utf-8 -*-
# LICENSE INFORMATION HERE
"""
GENERAL DOCUMENTATION HERE
"""

import platform
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
