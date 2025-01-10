#!/bin/python3

import sys
import os

def printAll(fileLine):
    print("==================")
    for i in range(len(fileLine)):
        print(f"{i + 1} | {fileLine[i]}")
    print("==================")

def write(filename, fileLine):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fileLine))
        f.close()

def ed_mode(filename):
    currentLns = 0
    toggleDisplay = True
    print("\nHINT: type .help to open help menu")
    append_mode = True
    if os.path.exists(filename):
        pass
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('')
            f.close()
    while True:
        # Create file if not exists
        # Read file
        with open(filename, 'r', encoding='utf-8') as f:
            f.seek(0)  
            file = f.read()
            fileLine = file.split('\n')
        
        if toggleDisplay:
            printAll(fileLine)
            
        # Read shell input
        shinput = input(f'[Ln {currentLns+1}] > ')
        if shinput in ('.nextline', '.nl'):
            currentLns += 1
            if currentLns + 1 > len(fileLine):
                fileLine.append(' ')
        elif shinput in ('.append', '.ap'):
            if append_mode:
                append_mode = False
                print("Disabled append mode")
            else:
                append_mode = True
                print("Enabled append mode")

        elif shinput in ('.show', '.s'):
            printAll()

        elif shinput in ('.toggled', '.t'):
            if toggleDisplay:
                print("Disabled file display")
                toggleDisplay = False
            else:
                print("Enabled file display")
                toggleDisplay = True
        
        # Prev line
        elif shinput in ('.prevline', '.pl'):
            currentLns -= 1

        # Clean all
        elif shinput in ('.cleanall', '.clearall', '.ca'):
            choice = input('Really? [Y/N] ')
            if choice.lower() == 'y':
                fileLine = ['']

            currentLns = 0

        elif shinput in ('.cleanline', '.clearline', '.cl'):
            choice = input(f'Really clean line {currentLns + 1}? [Y/N] ')
            if choice.lower() == 'y':
                fileLine[currentLns] = ''
        
        elif shinput in ('.quit', '.q'):
            f.close()
            write(filename, fileLine)
            exit()

        # Help Menu
        elif shinput in ('.help', '.h'):
            print("""
    .nextline , .nl
    .prevline , .pl
    .cleanall , .ca
    .cleanline, .cl
    .help     , .h
    .replace  , .r
    .show     , .s
    .toggled  , .t
    .quit     , .q
    .append   , .ap
            """)

        elif shinput in ('.replace', '.r'):
            target = input('Target? > ')
            replace = input('Replace? > ')

            fileLine[currentLns] = fileLine[currentLns].replace(target, replace)

        # Writing
        else:
            if append_mode:
                fileLine[currentLns] = fileLine[currentLns] + shinput
            else:
                fileLine[currentLns] = shinput

        f.close()
        write(filename, fileLine)

if __name__ == "__main__":
    print("\nOmegaEdit dev commit-16th")
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <filename>")
    else:
        print(f"Editing {sys.argv[-1]} as ed advanced mode.")
        ed_mode(sys.argv[-1])
