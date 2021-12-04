#!/usr/bin/env python3

import time, sys, InputParser
from ThreadsEnvironment import *

if __name__ == '__main__': # Disallow this script as a module

    if not '-h' in sys.argv or '--help' in sys.argv:
        print('[+] Loading the application environnement...')

    args = InputParser.InputParser(sys.argv)
    args = args.result

    # Init our environnement
    env = Environment(args["payload"], 
                    args["token"], 
                    args["path_pwd_list"], 
                    args["maxtries"], 
                    args["hash"], 
                    args["encoding"] , 
                    args["threads"], 
                    args["accurate"],
                    args["force"])
    
    def print_result():
        print(f'\n\n   [+] END OF PROCESS ({int(time.time()-env.INIT_TIME)} s)\n')
        print('   [FAILS] %s' % (env.FAILS))
        print('   [ERRORS] %s' % (env.ERROR))
        if env.FOUND == True:
            print('   [RESULT] Successful!')
            print("\n      > Password : '%s' (%s attempt for the thread that found)" % (env.FLAG, env.ATTEMPT))
            print('\n')
        else:
            print('   [RESULT] No success.')

    print('[+] Splitting %s words from the password list into %s lists for threads...' % (env.MAXTRIES, env.THREAD_NUMBER))


    try:
        env.thread_file_splitting()
        info_thread = InfoThread(env)

        # the job list 
        jobs = []

        print('[+] Creating %s threads...' % (env.THREAD_NUMBER))
        for i in range(env.THREAD_NUMBER):
            thread =  BruteForceThread(f"{env.TMP_PATH}{i}.txt", env)
            jobs.append(thread)
        print('\n\n   [+] STARTING %s research threads!\n\n' % (env.THREAD_NUMBER))
        info_thread.start()
        # Start the threads (i.e. brute force with each password list)
        for j in jobs:
            j.start()

        # Ensure all of the threads have finished
        for j in jobs:
            j.join()

    except KeyboardInterrupt:
        print("[STOPPED] Interrupted.")
        env.FOUND = None
    print_result()
    env.clean()
