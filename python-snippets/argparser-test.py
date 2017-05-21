#/usr/bin/python
#-*- encoding=utf-8 -*-

import argparse

class EntryRegister(object):
    COMMAND = 'reg'
    def add_args(self, parent_parser):
        parser = parent_parser.add_parser(self.COMMAND, help='backup help')
        parser.add_argument('-id', help='the id of entry')
        parser.add_argument('-desc', help='the desc of entry')
        parser.set_defaults(func=self)

    def __call__(self, args):
        print self.COMMAND, args.id, args.desc


class EntryUnregister(object):
    COMMAND = 'unreg'
    def add_args(self, parent_parser):

        parser = parent_parser.add_parser(self.COMMAND, help='unregister help')
        parser.add_argument('-id', help='the id of entry')
        parser.set_defaults(func=self)

    def __call__(self, args):
        print self.COMMAND, args.id

def main():
    parser = argparse.ArgumentParser(add_help=False)
    sub_parser = parser.add_subparsers(help='sub command help')

    command_processors = [
        EntryRegister(),
        EntryUnregister(),
    ]


    for processor in command_processors:
        processor.add_args(sub_parser)

    args = parser.parse_args('reg -id 10 -desc name'.split(' '))
    args.func(args)

    args = parser.parse_args('unreg -id 10'.split(' '))
    args.func(args)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()