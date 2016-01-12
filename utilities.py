#!/usr/bin/env python


def choice_error():
    print "Choice does not exist"


def end():
    exit(0)


def menu():
    print "=" * 33 + "\nMENU\n" + "=" * 33
    descriptions = ["Load host from external file",
                    "Print host list",
                    "Check active hosts",
                    "Select only running hosts",
                    "Select bots",
                    "Execute command locally",
                    "Execute command on bots",
                    "Open shell",
                    "Exit"]
    for num, func in enumerate(descriptions):
        print "[" + str(num) + "] " + func
    choice = raw_input(">>> ")
    return choice
