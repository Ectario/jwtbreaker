#!/usr/bin/env python3

USAGE = '''Usage : 


NAME
        jwtbreaker - Bruteforce JWT token with a password list

SYNOPSIS
        ./main.py [OPTIONS...] <token> <payload> <password_list_path> 
DESCRIPTION
        Try all passwords from the list passed in parameters.

        If the token to crack or the payload or the password list is missing from the parameters, return the usage.
        By default the hash algorithm is HS256.

        -h, --help
                Show usage.

        -m, --maxtries
                The maximum number of password we want to test

        -t, --threads
                Set the number of parallel processes that will work 

        -H, --hash
                Set the hash algorithm

        -e, --encoding
                Set the encoding in which to read the file with the list of passwords, by default it's 'latin-1'

        --accurate
                If set then the percentage, the fail number and the attempt number are accurate. But the Bruteforce go slowly.
                /!\ If you don't care about percentage then don't set it. /!\\
'''

from typing import Dict
import getopt
import sys, json, multiprocessing

class InputParser():
    def __init__(self, argv) -> None:
        self.result = self.__parse(argv)
        return None

    def __parse(self, argv) -> Dict:
        args_parsed : Dict = {}
        try:
            options, arguments = getopt.getopt(
                argv[1:],                      # Arguments
                'hm:t:H:e:',                            # Short option definitions
                ["help","accurate","maxtries=", "threads=", "hash=", "encoding="]) # Long option definitions

        except getopt.GetoptError as e:
            print(e)
            sys.exit(-1)
        
        for o, a in options:
            if o in ("-m", "--maxtries"):
                try:  
                    args_parsed['maxtries'] = int(a)
                except ValueError:
                    print("maxtries number must be an integer.")
            elif o in ("-t", "--threads"):
                try:
                    args_parsed['threads'] = int(a)
                except ValueError:
                    print("Threads number must be an integer.")
            elif o in ("-h", "--hash"):
                args_parsed['hash'] = str(a)
            elif o in ("-e", "--encoding"):
                args_parsed['encoding'] = str(a)    
            elif o in "--accurate":
                args_parsed['accurate'] = True
            elif o in ("-h", "--help"):
                print(USAGE)
                sys.exit(-1)

        if not arguments or len(arguments) != 3:
            raise SystemExit(USAGE)

        for i, e in enumerate(arguments):
            if i == 0:
                args_parsed["token"] = str(e)
            elif i == 1:
                try:
                    args_parsed["payload"] = json.loads(str(e))
                except ValueError:
                    print("The payload need to be like \"{\"first_property\":\"value\", \"second_property\":\"other_value\"}\"")
                    sys.exit(-1)
            elif i == 2:
                args_parsed["path_pwd_list"] = str(e)
        return self.__fillArgs(args_parsed)

    # Set the default values
    def __fillArgs(self, args : Dict) -> Dict:
        options = ["maxtries", "threads", "hash", "encoding", "payload", "token", "path_pwd_list", "accurate"]
        for e in options:
            if not str(e) in args:
                if str(e) == "maxtries":
                    args["maxtries"] = -1
                elif str(e) == "threads":
                    args["threads"] = int(multiprocessing.cpu_count())
                elif str(e) == "encoding":
                    args["encoding"] = 'latin-1'
                elif str(e) == "hash":
                    args["hash"] = 'HS256'
                elif str(e) == "accurate":
                    args["accurate"] = False
        self.__print_opt(args)
        return args

    def __print_opt(self, args_parsed):
        print()
        banner = "="*10 + " Configuration" + "="*10
        print(banner)
        for i in args_parsed:
            if i == "maxtries" and args_parsed['maxtries']==-1:
                print(f"[config] {i} = {args_parsed[i]} (ie. the entire passwordlist)")
                continue
            print(f"[config] {i} = {args_parsed[i]}")

        print("="*len(banner) + "\n")
