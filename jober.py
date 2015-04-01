#!/usr/bin/env python

import argparse
import json
import os
import random
import re
import sys

def wchoice(d):
    """Weighted version of random.choice
    """
    wlist = [(k, d[k]) for k in d]
    population = [val for val, cnt in wlist for i in range(int(cnt))]
    return random.choice(population)

def suckin(fname):
    """Open that fxxking file for reading
    """
    try:
        with open(fname, 'r+') as f:
            buf = f.read()
            if len(buf):
                return json.loads(buf)
            else:
                return {}
    except FileNotFoundError:
        raise FileNotFoundError

def spitout(fname, d):
    """Write changes into the file
    """
    with open(fname, 'w+') as f:
        f.write(json.dumps(d))

def main():
    """Parse arguments, dispatch, and error handling
    """
    parser = argparse.ArgumentParser(description='Provide some victims, with or without weights.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c',
                      '--create',
                      action='store_true',
                      help='create victim list')
    group.add_argument('-u',
                      '--user',
                      nargs=2,
                      metavar=('<username>', '<weight>'),
                      help='modified user with weight, create if not exist')
    group.add_argument('-d',
                      '--delete',
                      metavar='<username>',
                      help='delete user')
    group.add_argument('-p',
                      '--print',
                      action='store_true',
                      help='show the victims being selected in the list file')
    parser.add_argument('filename',
                       metavar='<filename>',
                       help='read from the file in JSON format')
    args = parser.parse_args()

    try:
        if args.create:
            if not os.path.isfile(args.filename):
                with open(args.filename, 'a') as f:
                    pass
            else:
                print('File already exist.')
                sys.exit(1)
        elif args.user:
            victims = suckin(args.filename)
            victims[args.user[0]] = args.user[1]
            spitout(args.filename, victims)
        elif args.delete:
            victims = suckin(args.filename)
            del victims[args.delete]
            spitout(args.filename, victims)
        elif args.print:
            victims = suckin(args.filename)
            print('{:<20}{:<}'.format('Username', 'Weight'))
            for k in victims:
                print('{:<20}{:<5}'.format(k, victims[k]))
        else:
            victims = suckin(args.filename)
            if victims:
                print('{:=^80}'.format(wchoice(victims)))
            else:
                print('Need at least one victim.')
                sys.exit(1)
    except FileNotFoundError:
        print('File not found.')
        sys.exit(1)
    except ValueError:
        print('Need JSON format file.')
        sys.exit(1)
    except KeyError:
        print('{} does not exist.'.format(args.delete))
        sys.exit(1)

if __name__ == '__main__':
    main()

