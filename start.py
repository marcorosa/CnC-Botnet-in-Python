#!/usr/bin/env python

from fabfile import *
from utilities import *


if __name__ == '__main__':
    df = {'0': load_hosts,
          '1': print_hosts,
          '2': check_hosts,
          '3': select_running_hosts,
          '4': choose_hosts,
          '5': run_locally,
          '6': run_command,
          '8': end}
    while True:
        choice = menu()
        df.get(choice, choice_error)()
