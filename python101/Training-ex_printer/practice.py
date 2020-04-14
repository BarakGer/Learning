# -*- coding: utf-8 -*-
import sys



def find_file_add(filename):
    scriptadd = sys.argv[0]
    folderadd = scriptadd[:scriptadd.rfind('/')]
    fileadd = folderadd + '/' + filename
    return fileadd


def print_file_content(fileadd):
    with open(fileadd) as filetoprint:
        for line in filetoprint:
            print line,


def main():
    filename = raw_input("please enter a file name\n")
    fileadd = find_file_add(filename)
    print_file_content(fileadd)

if __name__ == '__main__':
    main()
