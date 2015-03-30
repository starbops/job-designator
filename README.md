# job-designator

Randomly dispatch jobs, with weighted feature :grin:

## Usage

```
usage: jober.py [-h] [-c | -u <username> <weight> | -d <username>] <filename>

Provide some victims, with or without weights.

positional arguments:
  <filename>            read from the file in JSON format

optional arguments:
  -h, --help            show this help message and exit
  -c, --create          create victim list
  -u <username> <weight>, --user <username> <weight>
                        modified user with weight, create if not exist
  -d <username>, --delete <username>
                        delete user
```

