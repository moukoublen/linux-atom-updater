#!/usr/bin/env python3

import urllib
import urllib.request
import json
import os
import sys
import platform


def fix_path(path):
    return path if path[len(path)-1] == '/' else path + '/'


def get_github_data():
    url = "https://api.github.com/repos/atom/atom/releases/latest"
    response_str = urllib.request.urlopen(url).read().decode('utf-8')
    return json.loads(response_str)


def get_local_atom_version():
    return os.popen("atom -v | awk 'NR==1{print $3}'").read().split('\n')[0]


def get_package_name():
    packages = {}
    packages['fedora'] = 'atom.x86_64.rpm'
    packages['redhat'] = 'atom.x86_64.rpm'
    packages['centos'] = 'atom.x86_64.rpm'
    packages['suse'] = 'atom.x86_64.rpm'
    packages['ubuntu'] = 'atom-amd64.deb'
    packages['debian'] = 'atom-amd64.deb'
    distro = platform.linux_distribution(full_distribution_name=0)[0].lower()
    return packages[distro]


def get_install_command():
    commands = {}
    commands['fedora'] = 'dnf install '
    commands['ubuntu'] = 'apt install '
    distro = platform.linux_distribution(full_distribution_name=0)[0].lower()
    return commands[distro]


def get_download_link(latest_version):
    base_link = "https://github.com/atom/atom/releases/download"
    return "%s/v%s/%s" % (base_link, latest_version, get_package_name())


def download_atom_package(link, file_name):
    print("Downloading      : ", link)
    print("Download to      : ", file_name)
    data = urllib.request.urlopen(link).read()
    with open(file_name, 'wb') as out_file:
        out_file.write(data)


def install_atom_package(file_name):
    print("Installing package :", file_name)
    os.popen(get_install_command() + file_name).read()


def check_and_get_latest_atom(path_to_download="/tmp/"):
    json_data = get_github_data()
    latest_version = json_data['name']
    current_version = get_local_atom_version()
    print("Path to download : ", path_to_download)
    print("Current Version  : ", current_version)
    print("Latest  Version  : ", latest_version)
    if(current_version == latest_version):
        print("\nAtom is updated! No download is needed.")
    else:
        link = get_download_link(latest_version)
        file_name = path_to_download + get_package_name()
        download_atom_package(link, file_name)
        install_atom_package(file_name)
        os.remove(file_name)

#############################################################################

if os.getuid() != 0:
    print("This scrint must be run as root")
    exit()

if len(sys.argv) != 2:
    check_and_get_latest_atom()
else:
    check_and_get_latest_atom(fix_path(sys.argv[1]))
