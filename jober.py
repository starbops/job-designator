#!/usr/bin/env python
"""Pick up one victim from a list of victims with weight respectively

This tool helps you pick up a bad luck person from a list you provided. If you
don't like someone, you can increase the weight of the person. Then the person
with higher weight has higher chance being picked up.

Example:
    $ python jober.py -u alice 1
    $ python jober.py -u bob 5
    $ python jober.py vlist
    ================================someguytwo================================

"""

import argparse
import json
import os
import random
import sys

def wchoice(victims):
    """Weighted version of random.choice
    """
    wlist = [(k, victims[k]) for k in victims]
    population = [val for val, cnt in wlist for i in range(int(cnt))]
    return random.choice(population)

def suckin(fname):
    """Open that fxxking file for reading
    """
    try:
        with open(fname, 'r+') as fhdr:
            buf = fhdr.read()
            if len(buf):
                return json.loads(buf)
            else:
                return {}
    except FileNotFoundError:
        raise FileNotFoundError

def spitout(fname, victims):
    """Write changes into the file
    """
    with open(fname, 'w+') as fhdr:
        fhdr.write(json.dumps(victims))

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

    jober(args)

def jober(args):
    """Make decision (dispatching) according to the arguments
    """
    try:
        if args.create:
            if not os.path.isfile(args.filename):
                with open(args.filename, 'a'):
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
            sorted_victims = sorted(victims.items(), key=lambda x: x[1])
            print('{:<20}{:<}'.format('Username', 'Weight'))
            for (k, v) in sorted_victims:
                print('{:<20}{:<5}'.format(k, v))
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

