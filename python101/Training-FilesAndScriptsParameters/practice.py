# -*- coding: utf-8 -*-
def open_with_closing(filename):
    with open(filename, 'a') as fd1:
        fd1.write('I wouldn\'t do with it anything\n')


def main():
    open_with_closing(filename)
    with open(filename, 'r') as fd2:
        for line in fd2:
            print line,

if __name__ == '__main__':
    filename = r'C:\Heights\PortableApps\PortablePython2.7.6.1\App\hafifot\python101\temp_file.txt'
    main()