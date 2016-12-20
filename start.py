#!/usr/bin/env python

from botnet.fabfile import *
from botnet.utilities import *


if __name__ == '__main__':
    df = {'0': load_hosts,
          '1': add_host,
          '2': print_hosts,
          '3': check_hosts,
          '4': select_running_hosts,
          '5': choose_hosts,
          '6': run_locally,
          '7': run_command,
          '8': execute_script,
          '9': open_sh,
          '10': end}
    while True:
        choice = menu()
        df.get(choice, choice_error)()
