# jwtbreaker
jwtbreaker - Bruteforce JWT token with a password list

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PyJWT)
![PowerShell Gallery](https://img.shields.io/powershellgallery/p/DNS.1.1.1.1)

# Description
jwtbreaker allows you to bruteforce a token from a payload and a password list. By default, jwtbreaker uses all the available cores of the computer which allows parallel processing of passwords and maximizes the speed of calculation and tests.

# Requirements

- [Python 3](https://www.python.org/downloads/)
- [PyJWT (python 3 module)](https://pypi.org/project/PyJWT/)

# Installation

## Download
The files can either be downloaded directly (the download zip in the clone menu) or can be cloned if you have git available:

 `git clone https://github.com/Ectario/jwtbreaker.git`

## Setup
Go to the jwtbreaker directory: `cd jwtbreaker`.

To authorize the execution of the code under macOS/Linux: `chmod +x ./main.py`

_note: for Windows systems you just have to make sure that python3 is in the path_

# Usage
### General usage (macOS/Linux): `./main.py [OPTIONS...] <token> <payload> <password_list_path>`
_note: under Windows there are the same commands but without './'_


- __Get help__
  `./main.py -h` or `./main.py --help`

- `-H/--hash` - __Set hashing algorithm for the token__  _(Default : HS256)_

  `./main.py -H HS512 <token> <payload> <password_list_path>`

  or

  `./main.py --hash=HS512 <token> <payload> <password_list_path>`

  _HS512 is an example._


- `-m/--maxtries` - __Set the maximum number of tries before the program stops__ _(Default : the whole list)_
 
  `./main.py -m 10 <token> <payload> <password_list_path>`
 
  or

  `./main.py --maxtries=10 <token> <payload> <password_list_path>`
 

- `-t/--threads` - __Set the thread number__ _(Default : number of cores on machine)_

  `./main.py -t 4 <token> <payload> <password_list_path>`
 
  or

  `./main.py --threads=4 <token> <payload> <password_list_path>`
 

- `-e/--encoding` - __Set the encoding used to read the password list)__ _(Default : latin-1)_

  `./main.py -e utf-8 <token> <payload> <password_list_path>`
 
  or

  `./main.py --encoding=utf-8 <token> <payload> <password_list_path>`
 
- `--force` - __Allows to ignore the byte read errors coming from the passwordlist. This is the force-mode.__

    `./main.py --force <token> <payload> <password_list_path>`

    _It is possible not to use all the words in the password list since some of them have been skipped due to a byte reading error._

- `--accurate` - __If it is necessary to have a good precision on the percentage or the number of tests which were made__
 
    `./main.py --accurate <token> <payload> <password_list_path>`
    
    _The threads can occasionally overlap during incrementation which sometimes skews the data. This flag allows the use of mutexes so that the threads do not overlap (only) during incrementations._
    
    _**Be careful!** Using this flag slows down the program._
    

Of course it is possible to chain as many options as you want (it is enough that the options are before the mandatory part of the token, payload and password list).

# Example


        ~/jwtbreaker$ ./main.py -t 4 "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6InRydWUifQ.mpfL_UMUlKsmlGiQaHEeymiSaQmych9R6t0soV5qCaw" "{\"admin\":\"true\"}" "../../passwordlist/rockyou.txt"
        [+] Loading the application environnement...
        
        ========== Configuration ==========
        [config] threads = 4
        [config] token = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhZG1pbiI6InRydWUifQ.mpfL_UMUlKsmlGiQaHEeymiSaQmych9R6t0soV5qCaw
        [config] payload = {'admin': 'true'}
        [config] path_pwd_list = ../../passwordlist/rockyou.txt
        [config] maxtries = -1 (ie. the entire passwordlist)
        [config] hash = HS256
        [config] encoding = latin-1
        [config] accurate = False
        ==================================
        
        [+] Splitting 14344391 words from the password list into 4 lists for threads...
        [+] Creating 4 threads...
        
        
           [+] STARTING 4 research threads!
        
        
        [INFO] 0 %
        
        
           [+] END OF PROCESS (24 s)
        
           [FAILS] 75571
           [ERRORS] 0
           [RESULT] Successful!
        
          	> Password : 'admin' (19821 attempt for the thread that found)


