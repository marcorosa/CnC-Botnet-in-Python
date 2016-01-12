#!/usr/bin/env python

from fabric.api import env, run, sudo, execute, local
import paramiko
from tabulate import tabulate


paramiko.util.log_to_file("paramiko.log")
env.colorize_errors = True
# The selected hosts are the hosts in env (at the beginning)
selected_hosts = env.hosts
running_hosts = {}


def load_hosts():
    """
    Load hosts from hosts.txt. A host can either be in form
    username@host password
        or
    username@hotst
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
    hosts = map(lambda x: [x], env.hosts)
    print tabulate(hosts, ["Host"])


def check_hosts():
    global running_hosts
    global selected_hosts
    running_hosts = dict()
    selected_hosts = []
    for host, result in execute(execute_command, "uptime", hosts=env.hosts).iteritems():
        if result.succeeded:
            running_hosts[host] = True
            selected_hosts.append(host)
        else:
            running_hosts[host] = False
    print_dict_table(running_hosts)


def print_dict_table(d):
    mylist = map(lambda index: [index[0], index[1]], d.items())
    print tabulate(mylist, ["Host", "Running"])


def print_selected_hosts():
    check_hosts()
    print "Selected hosts:"
    print "-" * 25
    # selectedList = map(lambda index: [index[0], index[1]], selected_hosts.items())
    # print tabulate(selectedList, ["Host", "Running"])


def select_hosts():
    pass


def execute_command(command):
    if command.strip()[:5] == "sudo":
        results = sudo(command, shell=False)
    else:
        results = run(command)
    return results


def run_command():
    cmd = raw_input("Insert command: ")
    execute(execute_command, cmd, hosts=selected_hosts)


def run_locally():
    cmd = raw_input("Insert command: ")
    local(cmd)
