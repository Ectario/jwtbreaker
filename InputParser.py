#!/usr/bin/env python3

USAGE = '''

Usage : 


NAME
        jwtbreaker - Bruteforce JWT token with a password list

SYNOPSIS
        ./main.py <token> <payload> <password_list_path> [OPTIONS]...

DESCRIPTION
        Try all the passwords in the list passed in parameters.

        If the token to crack or the payload or the password list is missing from the parameters, return the usage.
        By default the hash algorithm is HS256.


        -a, --attempt
                The maximum number of password we want to test

        -t, --threads
                Set the number of parallel processes that will work 

        -h, --hash
                Set the hash algorithm

        -e, --encoding
                Set the encoding in which to read the file with the list of passwords, by default it's 'latin-1'

'''

from typing import Dict
from getopt import getopt


class InputParser():
    def __init__(self, argv) -> Dict:
        args_parsed : Dict = {}
        options, arguments = getopt.getopt(
            argv[1:],                      # Arguments
            'athe:',                            # Short option definitions
            ["attempt", "threads", "hash", "encoding"]) # Long option definitions
        for o, a in options:
            if o in ("-a", "--attempt"):
                try:  
                    args_parsed['attempt'] = int(a)
                except ValueError:
                    print("Attempt number must be an integer.")
            elif o in ("-t", "--threads"):
                try:
                    args_parsed['threads'] = int(a)
                except ValueError:
                    print("Threads number must be an integer.")
            elif o in ("-h", "--hash"):
                args_parsed['hash'] = str(a)
            elif o in ("-e", "--encoding"):
                args_parsed['encoding'] = str(a)    

        if not arguments or len(arguments) != 3:
            raise SystemExit(USAGE)



        return {}