import argparse              # add debugging
import getpass               # this has not be tested with a deb system
import os
import logging
import time

DEBUG_FILE = None
MODE = None
REDHAT = None
FILEPATH = None
PASSWORD = None
__version__ = "0.1.0"


def main():
    global PASSWORD

    set_debug_file()
    get_commands()

    PASSWORD = getpass.unix_getpass("Please enter your password: ")

    if MODE == "redhat":
        temp = read_file()
        red_hat_install(temp)
    else:
        temp = read_file()
        auto(temp)


def auto(list_of_command):
    my_switch = True
    i = 0

    while my_switch:
        try:
            command = " apt-get -y update"
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))

            command = " apt-get -y install " + list_of_command[i]
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))
        except IndexError:
            my_switch = False

        i = i + 1


def get_commands():
    global MODE
    global FILEPATH

    parser = argparse.ArgumentParser(version=__version__, description="Auto install a list of packages from a text"
                                                                      " file")
    parser.add_argument('-a', '--auto', action="store", help='use this if you are using a deb system also enter a path'
                                                             ' to text file need')
    parser.add_argument('-r', '--redhat', action="store", help='use this if you are using a rpm system also enter a'
                                                               ' path to the text file')

    my_Arg = parser.parse_args()

    if my_Arg.auto:
        MODE = "auto"
        FILEPATH = my_Arg.auto

    if my_Arg.redhat:
        MODE = "redhat"
        FILEPATH = my_Arg.redhat


def set_debug_file():
    global DEBUG_FILE

    temp = os.getenv("HOME")
    temp2 = "/.mulvie/"
    temp3 = "linux_install/"
    filename = "log.txt"

    t = temp + temp2
    tt = t + temp3

    if os.path.isdir(t):
        pass
    else:
        os.mkdir(t)

    if os.path.isdir(tt):
        pass
    else:
        os.mkdir(tt)

    DEBUG_FILE = temp + temp2 + temp3 + filename

    logging.basicConfig(filename=DEBUG_FILE, filemode='a', level=logging.DEBUG)


def read_file():
    my_list = []

    with open(FILEPATH) as f:
        for line in f:
            my_list.append(line)

    return my_list


def red_hat_install(list_of_packages):
    my_switch = True
    i = 0

    while my_switch:
        try:
            command = "yum -y update"
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))

            command = "yum -y install " + list_of_packages[i]
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))
        except IndexError:
            my_switch = False

        i = i + 1


if __name__ == '__main__':
    main()