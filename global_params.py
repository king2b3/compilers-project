""" Global declarations for the compiler.
    Mostly used to print colors to the console. 

    Created on: 1-30-2021
    Version: Python 3.8.5
    Created by: Bayley King (https://github.com/king2b3)
"""
#print(f"{bcolors['WARNING']}Warning: No active frommets remain. Continue?{bcolors['ENDC']}")
bcolors = {
    'HEADER':'\033[95m',
    'OKBLUE':'\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}
