#!/usr/bin/env python

from fabfile import *
from utilities import *


if __name__ == '__main__':
    df = {'0': load_hosts, '1': print_hosts, '2': print_selected_hosts,
          '3': select_hosts, '4': run_locally, '5': run_command, '7': end}
    while True:
        choice = menu()
        df.get(choice, choice_error)()
