import argparse
import os
import sys



def main():
    args = sys.argv[1:]
    if args:
        print(f'arg name: {args[0]}, arg val: {args[1]}')
    else:
        print('no args passed')


main()