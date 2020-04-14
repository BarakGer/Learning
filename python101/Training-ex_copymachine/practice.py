# -*- coding: utf-8 -*-
def copy_file(Origin, Copy):
    '''  copies the Origin file contents into the file Copy '''
    Copy.write(Origin.read())


def main():
    Origin_File = r'C:\Heights\PortableApps\PortablePython2.7.6.1\App\hafifot\python101\origin_file.txt'
    Copy_File = r'C:\Heights\PortableApps\PortablePython2.7.6.1\App\hafifot\python101\copy_file.txt'
    with open(Origin_File, 'r') as Origin:
        with open(Copy_File, 'a') as Copy:
            copy_file(Origin, Copy)


main()