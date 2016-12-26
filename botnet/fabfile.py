#!/usr/bin/env python

import os
from fabric.api import env, run, sudo, execute, local, settings, hide, open_shell, parallel
from fabric.contrib.console import confirm
import paramiko
import getpass
from tabulate import tabulate


file_hosts = "hosts.txt"
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
    with open(file_hosts, "r") as f:
        data = f.readlines()
        for line in data:
            try:
                host, password = line.strip().split()
            except ValueError:
                host = line.strip()
                password = None
            if len(host.split(':')) == 1:
                host = host + ":22"
            env.hosts.append(host)
            if password is not None:
                env.passwords[host] = password.strip()


def add_host():
    """
    Add a new host to the running hosts.
    Add the new host also to the external host file.
    """
    name = raw_input("Username: ")
    host = raw_input("Host: ")
    port = input("Port: ")
    new_host = name + "@" + host + ":" + str(port)
    selected_hosts.append(new_host)
    password = None
    if confirm("Authenticate using a password "):
        password = getpass.getpass("Password: ").strip()
        env.passwords[new_host] = password

    # Append the new host to the hosts file
    if confirm("Add the new host to the hosts file? "):
        if password is not None:
            line = new_host + " " + password + "\n"
        else:
            line = new_host + "\n"
        with open(file_hosts, 'a') as f:
            f.write(line)


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
    for host in selected_hosts:
        print "\nPing host " + str(selected_hosts.index(host) + 1) + " of " + str(len(selected_hosts))
        response = os.system("ping -c 1 " + host.split("@")[1].split(":")[0])
        if response == 0:
            running_hosts[host] = True
        else:
            running_hosts[host] = False
    # Convert running_hosts in order to print it as table
    mylist = map(lambda index: [index[0], str(index[1])], running_hosts.items())
    print tabulate(mylist, ["Host", "Running"])


def select_running_hosts():
    """
    Select all running hosts.
    """
    global selected_hosts
    with hide('stdout'):
        check_hosts()
    host_up = filter(lambda x: running_hosts.get(x, False), running_hosts.keys())
    selected_hosts = host_up


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


@parallel
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


def run_locally(cmd=None):
    """
    Execute a command locally.
    """
    if cmd is None:
        cmd = raw_input("Insert command: ")
    with settings(warn_only=True):
        local(cmd)


@parallel
def run_command(cmd=None):
    """
    Execute a command on a host.
    """
    if cmd is None:
        cmd = raw_input("Insert command: ")
    execute(execute_command, cmd, hosts=selected_hosts)


def execute_script():
    script_file = raw_input("Name of the script: ")
    host_path = "/tmp"
    # Copy the script on bots
    for h in selected_hosts:
        with hide('stdout', 'running'):
            run_locally('scp %s %s:%s' % (script_file, h.split(':')[0], host_path))
    # Execute script
    run_command(host_path + "/" + script_file)
    # Delete script
    with hide('running'):
        run_command("rm " + host_path + "/" + script_file)


def open_sh():
    mylist = map(lambda (num, h): [num, h], enumerate(selected_hosts))
    print tabulate(mylist, ["Number", "Host"])
    n = input("Open shell in host number: ")
    try:
        h = selected_hosts[n]
        execute(open_shell, host=h)
    except Exception:
        print "Error. Shell not opened."
