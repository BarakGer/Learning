# -*- coding: utf-8 -*-
import os


def main():
    if os.path.isdir(directory):
        print os.listdir(directory)
    else:
        print 'the system cannot find this path'


if __name__ == '__main__':
    directory = 'C:\Heights\PortableApps\PortablePython2.7.6.1\App\hafifo\python101'
    main()