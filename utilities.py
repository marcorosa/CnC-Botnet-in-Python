#!/usr/bin/env python


def choice_error():
    print "Choice does not exist"


def end():
    exit(0)


def menu():
    print "=" * 33 + "\nMENU\n" + "=" * 33
    descriptions = ["Load host from external file",
                    "Add a new host",
                    "Print selected hosts",
                    "Check active hosts",
                    "Select only active hosts",
                    "Select bots",
                    "Execute command locally",
                    "Execute command on bots",
                    "Run external script",
                    "Open shell in a host",
                    "Exit"]
    for num, func in enumerate(descriptions):
        print "[" + str(num) + "] " + func
    choice = raw_input(">>> ")
    return choice
