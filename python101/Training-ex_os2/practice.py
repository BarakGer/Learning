# -*- coding: utf-8 -*-
import os


def open_and_solve(filename):
    # opens file and solves the exrecises
    sol_file = open("solutions.txt","a+")
    with open(filename, 'r') as exrecises:
        for line in exrecises:
            sol, isOK = understand_ex(line)
            if isOK:
                sol_file.write(line.rstrip() + ' = ' + str(sol) + '\n')



def is_ex_ok(line):
    num_spaces = 0
    num_actions = 0
    num_digits = 0
    isOK = True
    for char in line:
        if char in '+-*/':
            num_actions += 1
            action_index = line.find(char)
        elif char == ' ':
            num_spaces += 1
        elif char.isdigit():
            num_digits +=1
        elif char == '\n':
            pass
        else:
            isOK = False
    if num_digits <2 or num_spaces != 2 or num_actions != 1 or not(line[action_index-1].isspace()) or not(line[action_index+1].isspace()):
        isOK = False
    return isOK


def understand_ex(line):
    isOK = is_ex_ok(line)
    sol = 0
    if isOK:
        num1 = float(line[:line.find(' ')])
        symbol = line[line.find(' ')+1]
        num2 = float(line[line.rfind(' ')+1:])
        if symbol == '+':
            sol = num1 + num2
        elif symbol == '-':
            sol = num1 - num2
        elif symbol == '*':
            sol = num1 * num2
        elif symbol == '/':
            sol = num1 / num2
        else:
            isOK = False
    return sol, isOK

def input_check():
    #does file exists
    if os.path.isfile(ex_file):
        file_exists = True
    else:
        file_exists = False
        print 'the system cannot find this file'
    return file_exists


def main():
    if input_check():
        open_and_solve(ex_file)


if __name__ == '__main__':
    ex_file = 'C:\Heights\PortableApps\PortablePython2.7.6.1\App\hafifot\python101\ex_file.txt'
    main()