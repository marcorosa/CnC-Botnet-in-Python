import sys


def choice_error():
    """Print an error message in case the user selects a wrong action."""
    print('Choice does not exist')


def end():
    """Terminate the execution."""
    sys.exit(0)


def menu():
    """Print a menu with all the functionalities and return the user's choice
    """
    print('=' * 33, '\nMENU\n', '=' * 33)
    descriptions = ['Load host from external file',
                    'Add a new host',
                    'Print selected hosts',
                    'Check active hosts',
                    'Select only active hosts',
                    'Select bots',
                    'Execute command locally',
                    'Execute command on bots',
                    'Run external script',
                    'Open shell in a host',
                    'Exit']
    for num, func in enumerate(descriptions):
        print(f'[{num}] {func}')
    choice = input('>>> ')
    return choice
