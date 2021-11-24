#!/usr/bin/env python3

import time
from ThreadsEnvironment import *

if __name__ == '__main__': # Disallow this script as a module

    # Init our environnement

    params = {'username':'Ectario', 'admin':'false'}
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkVjdGFyaW8iLCJhZG1pbiI6ZmFsc2V9.vojYa2zg0JAw4lpuugVyxc_PR7igtdeuT6i6JCfYKJ4"



    # tries, params, token, path_pwd_list, hashing_algorithm = 'HS256', encoding_pwd_file = 'utf-8', thread_number = 4

    print('[+] Loading the application environnement...')

    env = Environment(-1, params, token, "../../passwordlist/rockyou.txt", 'HSfd256', thread_number=4)

    def print_result():
        print(f'\n\n   [+] END OF PROCESS ({int(time.time()-env.INIT_TIME)} s)\n')
        print('   [FAILS] %s' % (env.FAILS))
        if env.FOUND == True:
            print("\n      > Password : '%s' (%s attempt for the thread that found)" % (env.FLAG, env.ATTEMPT))
            print('\n')


    print('[+] Splitting %s the password list into %s lists for threads...' % (env.TRIES, env.THREAD_NUMBER))

    env.thread_file_splitting()
    info_thread = InfoThread(env)
    info_thread.setDaemon(True)

    # the job list 
    jobs = []

    print('[+] Creating %s threads...' % (env.THREAD_NUMBER))
    for i in range(env.THREAD_NUMBER):
        thread =  BruteForceThread(f"{env.TMP_PATH}{i}.txt", env)
        jobs.append(thread)
    try:
        print('\n\n   [+] STARTING %s research threads!\n\n' % (env.THREAD_NUMBER))
        info_thread.start()
        # Start the threads (i.e. brute force with each password list)
        for j in jobs:
            j.start()

        # Ensure all of the threads have finished
        for j in jobs:
            j.join()
        
        time.sleep(0.001)
    except KeyboardInterrupt:
        print("[STOPPED] Interrupted.")
        env.FOUND = None
    print_result()
    env.clean_tmp()
