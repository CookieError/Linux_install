import argparse
import getpass               # this has not be tested with a deb system / change auto to debian
import os                    # add an if so the update and upgrade will not run everytime
import logging
import time
import datetime

DEBUG_FILE = None
MODE = None
REDHAT = None
FILEPATH = None
PASSWORD = None
__version__ = "0.1.0"


def main():
    global PASSWORD

    set_debug_file()
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' setting up log successful ')
    get_commands()
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' asking the user for there password ')
    PASSWORD = getpass.unix_getpass("Please enter your password: ")

    if MODE == "redhat":
        logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' MODE was set to readhat ')
        temp = read_file()
        logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' reding from text file was successful ')
        red_hat_install(temp)

    elif MODE == "debian":
        logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' MODE was set to debian ')
        temp = read_file()
        logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' reading from text file was successful ')
        debian_install(temp)


def debian_install(list_of_command):
    my_switch = True
    i = 0
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' about to run debian_install() ')

    while my_switch:
        try:
            command = " apt-get -y update"
            logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' about to run ' + str(command))
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))

            command = " apt-get -y upgrade " + list_of_command[i]
            logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' about to run ' + str(command))
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))

            command = " apt-get -y install " + list_of_command[i]
            logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' about to run ' + str(command))
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))
        except IndexError:
            my_switch = False

        i = i + 1


def get_commands():
    global MODE
    global FILEPATH

    parser = argparse.ArgumentParser(version=__version__, description="Auto install a list of packages from a text"
                                                                      " file")
    parser.add_argument('-d', '--debian', action="store", help='use this if you are using a debian system also enter a path'
                                                             ' to text file need')
    parser.add_argument('-r', '--redhat', action="store", help='use this if you are using a rpm system also enter a'
                                                               ' path to the text file')

    my_Arg = parser.parse_args()

    if my_Arg.debian:
        MODE = "debian"
        FILEPATH = my_Arg.debian

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
    logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' about to run red_hat_install() ')

    while my_switch:
        try:
            command = "yum -y update"
            logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' about to run ' + str(command))
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))

            command = "yum -y install " + list_of_packages[i]
            logging.debug(str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + ' about to run ' + str(command))
            p = os.system('echo %s|sudo -S %s' % (PASSWORD, command))
        except IndexError:
            my_switch = False

        i = i + 1


if __name__ == '__main__':
    main()