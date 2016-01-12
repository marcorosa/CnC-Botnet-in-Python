#!/usr/bin/env python

from fabric.api import env, run, sudo, execute, local, settings, hide
import paramiko
from tabulate import tabulate


paramiko.util.log_to_file("paramiko.log")
env.colorize_errors = True
# The selected hosts are the hosts in env (at the beginning)
selected_hosts = env.hosts
running_hosts = {}


def load_hosts():
    """
    Load hosts from hosts.txt.
    A host can either be in form
    username@host[:port] password
        or
    username@host[:port]
    If no port is specified, port 22 is selected.
    """
    with open("hosts.txt", "r") as f:
        data = f.readlines()
        for line in data:
            try:
                host, password = line.strip().split()
            except Exception:
                host = line.strip()
                password = None
            if len(host.split(':')) == 1:
                host = host + ":22"
            env.hosts.append(host)
            if password is not None:
                env.passwords[host] = password.strip()


def print_hosts():
    """
    Print selected hosts.
    If you haven't hand-select hosts yet, all hosts are selected.
    """
    global selected_hosts
    hosts = map(lambda x: [x, env.passwords.get(x, None)], selected_hosts)
    print tabulate(hosts, ["Host", "Password"])


def check_hosts():
    """
    Check if hosts are running or not.
    """
    global running_hosts
    running_hosts = dict()
    with hide('stdout'):
        for host, result in execute(execute_command, "uptime", hosts=env.hosts).iteritems():
            if result.succeeded:
                running_hosts[host] = True
            else:
                running_hosts[host] = False
    # Convert running_hosts in order to print it as table
    mylist = map(lambda index: [index[0], index[1]], running_hosts.items())
    print tabulate(mylist, ["Host", "Running"])


def select_running_hosts():
    """
    Select all running hosts.
    """
    global selected_hosts
    with hide('stdout'):
        check_hosts()
    selected_hosts = running_hosts.keys()


def choose_hosts():
    """
    Select hosts you want to use.
    """
    global selected_hosts
    selected_hosts = []
    mylist = map(lambda (num, h): [num, h], enumerate(env.hosts))
    print "Select Hosts:"
    print tabulate(mylist, ["Number", "Host"])
    choices = raw_input("> ").split()
    # Avoid letters in string index
    choices = filter(lambda x: x.isalnum(), choices)
    # Convert to int list
    choices = map(lambda x: int(x), choices)
    # Avoid IndexError
    choices = filter(lambda x: x < len(env.hosts), choices)
    # Get only selected hosts
    selected_hosts = map(lambda i: env.hosts[i], choices)


def execute_command(command):
    """
    Execute a command on a host.
    """
    with settings(warn_only=True):
        if command.strip()[:5] == "sudo":
            results = sudo(command, shell=False)
        else:
            results = run(command)
        return results


def run_locally():
    """
    Execute a command locally.
    """
    cmd = raw_input("Insert command: ")
    with settings(warn_only=True):
        local(cmd)


def run_command():
    """
    Execute a command on a host.
    """
    cmd = raw_input("Insert command: ")
    execute(execute_command, cmd, hosts=selected_hosts)
