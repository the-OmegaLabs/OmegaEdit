#!/bin/python3

import sys
import os
import utils.CursorLibs as Curs

def printAll(fileLine, currentLns):
    print("==================")
    for i in range(len(fileLine)):
        if i == currentLns:
            currentSign = '>'
        else:
            currentSign = ' '
        lineString = f"{i + 1}".ljust(len(str(len(fileLine))))
        #lineString = i + 1
        print(f"{currentSign} {lineString} | {fileLine[i]}")
    print("==================")

def write(filename, fileLine):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fileLine))
        f.close()

def ed_mode(filename):
    print("HINT: type .help to open help menu")
    print("      You can exit the editor with .quit/.q command.")
    currentLns = 0
    toggleDisplay = True
    toggleClean = True
    toggleAppend = True
    if os.path.exists(filename):
        pass
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('')
            f.close()
    while True:
        # Read file
        with open(filename, 'r', encoding='utf-8') as f:
            f.seek(0)  
            file = f.read()
            fileLine = file.split('\n')

        print(f"Editing {filename}.")

        if toggleDisplay:
            printAll(fileLine, currentLns)
            
        # Read shell input
        shinput = input(f'I {currentLns+1} > ')
        if shinput in ('.nextline', '.n'):
            currentLns += 1
            if currentLns + 1 > len(fileLine):
                fileLine.append(' ')
        elif shinput.startswith('.goto') or shinput.startswith('.g'):
            gotoLns = shinput.split(' ')[-1]
            if gotoLns.isdigit() and int(gotoLns) - 1 < len(fileLine):
                currentLns = int(gotoLns) - 1

        
        elif shinput in ('.append', '.ta'):
            if toggleAppend:
                toggleAppend = False
                print("Disabled append mode")
            else:
                toggleAppend = True
                print("Enabled append mode")

        elif shinput in ('.show', '.s'):
            pass

        elif shinput in ('.display', '.td'):
            if toggleDisplay:
                print("Disabled file display")
                toggleDisplay = False
            else:
                print("Enabled file display")
                toggleDisplay = True
        
        # Prev line
        elif shinput in ('.prevline', '.p'):
            currentLns -= 1

        # Clean all
        elif shinput in ('.cleanall', '.clearall', '.ca'):
            choice = input('Really clean all lines? [Y/N] ')
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
            break
    
        elif shinput in ('.autoclean', '.tc'):
            if toggleDisplay:
                print("Disabled auto clean screen")
                toggleDisplay = False
            else:
                print("Enabled auto clean screen")
                toggleDisplay = True

        # Help Menu
        elif shinput in ('.help', '.h'):
            print("""
    .goto     , .g <line>
    .nextline , .n
    .prevline , .p
    .help     , .h
    .replace  , .r
    .show     , .s
    .quit     , .q
    .cleanall , .ca
    .cleanline, .cl
    .display  , .td
    .append   , .ta
    .autoclean, .tc
            """)

        elif shinput in ('.replace', '.r'):
            target = input('Target ? ')
            replace = input('Replace as ? ')

            fileLine[currentLns] = fileLine[currentLns].replace(target, replace)

        # Writing
        else:
            if toggleAppend:
                fileLine[currentLns] = fileLine[currentLns] + shinput
            else:
                fileLine[currentLns] = shinput

        if toggleClean:
            Curs.clear_screen()
        
        f.close()
        write(filename, fileLine)

if __name__ == "__main__":
    print("\nOmegaEdit dev commit-16th")
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <filename>")
    else:
        ed_mode(sys.argv[-1])
