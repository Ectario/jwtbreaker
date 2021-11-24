#!/usr/bin/env python3

import sys
import shutil
import threading
import time
import threading
import time
import jwt
import os

class Environment():
    def __init__(self, tries, params, token, path_pwd_list, hashing_algorithm = 'HS256', encoding_pwd_file = 'latin-1', thread_number = 4):
        self.TOKEN = token
        self.PARAMS = params
        self.HASH = hashing_algorithm
        self.ENCODING_PWD_FILE = encoding_pwd_file
        self.PATH = path_pwd_list  # Path of password list
        self.TMP_PATH = "./tmp/"  # Created during the runtime -> store the files for each Thread
        self.FAILS, self.ERROR = 0, 0
        self.FLAG = ''
        self.TRIES = tries  # Password number to check : WARNING -> percentage not accurate if too big
        self.FOUND = False
        self.THREAD_NUMBER = thread_number # Warning too much thread can be more slower (the computer need to manage them so his capacities are used)
        self.FILES_PATHS = []  # Each thread has his file
        self.ATTEMPT = 0
        self.THREAD_PERCENTAGE = None
        self.INIT_TIME = time.time()
        # Get the line number of the file
        if tries == -1:
            try:
                with open(self.PATH, encoding=encoding_pwd_file) as f:
                    file = f.readlines()
                    self.TRIES = len(file)
            except UnicodeDecodeError:
                print('[+] Wrong encoding for the password file \'%s\'. Try to use -e or --encoding with the right encoding (ex: utf-8, utf-16, ascii...).' % self.ENCODING_PWD_FILE)
                sys.exit(-1)
            except Exception:
                print('[+] Encoding for the password file \'%s\' doesn\'t exists.' % self.ENCODING_PWD_FILE)
                sys.exit(-1)

     # Create for each thread -> his password list
    def thread_file_splitting(self):
        try:
            os.mkdir("./tmp")
        except:
            pass
        try:
            with open(self.PATH, 'r',encoding=self.ENCODING_PWD_FILE) as f:
                current_number_thread = 0
                data = ""
                for i in range(self.TRIES):
                    line = f.readline().strip()
                    data += line+"\n"
                    # Checking if it's the moment to split (example : if THREAD_NUMBER = 2 and TRIES = 10, we write/split to an other file at i=5 to i=10)
                    if (i-1 != 0 and (i-1) % int(self.TRIES/self.THREAD_NUMBER) == 0) or i+1 == self.TRIES:
                        new_path = f"{self.TMP_PATH}{str(current_number_thread)}.txt"
                        with open(new_path, 'w') as f_tmp:
                            current_number_thread += 1
                            f_tmp.write(data)
                            f_tmp.close()
                        self.FILES_PATHS.append(new_path)
                        data = ""
        
        except UnicodeDecodeError:
            print('[+] Wrong encoding for the password file [%s]. Try to use -e or --encoding with the right encoding (ex: utf-8, utf-16, ascii...).' % self.ENCODING_PWD_FILE)
            sys.exit(-1)

        except Exception:
            print('[+] Encoding for the password file \'%s\' doesn\'t exists.' % self.ENCODING_PWD_FILE)
            sys.exit(-1)

    # Delete file_splitting tmp files
    def clean_tmp(self):
        shutil.rmtree("tmp")



class BruteForceThread(threading.Thread):
    def __init__(self, path, env : Environment):
        threading.Thread.__init__(self)
        self.env = env
        self.path = path
    def run(self):  # path is the file path for the thread using this function. Brute Force basic auth function.
        # print('\n\n   [+] STARTING \'%s\'\n\n' % (self.env.))
        with open(self.path, 'r') as f:
            for i in range(int(self.env.TRIES/self.env.THREAD_NUMBER)):
                if self.env.FOUND == False:
                    PSW = f.readline().strip()  # Getting password (1 line = 1 password)
                    self.env.ATTEMPT += 1
                    try:
                        r = jwt.encode(self.env.PARAMS, PSW, algorithm=self.env.HASH)
                        if r == self.env.TOKEN:  
                            self.env.ATTEMPT = i + 1
                            self.env.FLAG = PSW
                            self.env.FOUND = True
                            break
                        self.env.FAILS += 1
                    except Exception as e:  # Catch problem
                        print('[ERROR] SOMETHING WENT WRONG')
                        self.env.ERROR += 1
                        if self.env.ERROR > 10 and self.env.FOUND!=None:
                            self.env.FOUND = None
                            print('[FATAL ERROR] Too much errors.')
                            print()
                            print(e)
                            print()
                            sys.exit(-1)
                else:
                    break


class InfoThread(threading.Thread):
    def __init__(self, env : Environment):
        threading.Thread.__init__(self)
        self.env = env
    def run(self):
        last_percentage = -1
        current_percentage = self.get_percentage()
        while current_percentage<101 or self.env.FOUND!=True:
            current_percentage = self.get_percentage()
            if last_percentage != current_percentage and current_percentage<101:
                print(f"[INFO] {current_percentage} %")
                last_percentage=current_percentage
            time.sleep(0.001)
    def get_percentage(self):
        return int(float(self.env.ATTEMPT)*100 / float(self.env.TRIES))