#!/bin/python3

import sys
import os

def ed_mode(filename):
    currentLns = 0
    while True:
        # Create file if not exists
        if os.path.exists(filename):
            pass
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('')
                f.close()
        # Read file
        with open(filename, 'r', encoding='utf-8') as f:
            f.seek(0)  
            file = f.read()
            fileLine = file.split('\n')
            print("\n==================")
            print(filename)
            print("==================")
            for i in range(len(fileLine)):
                print(f"{i+1} | {fileLine[i]}")
            print("==================")
        # Input Module
        while True:
            # Read shell input
            shinput = input(f'[Ln {currentLns+1}] > ')
            if shinput in ('.nextline', '.nl'):
                currentLns += 1
                fileLine.append(' ')
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(fileLine))
                    f.close()
                    break
                break
            # Prev line
            elif shinput in ('.prevline', '.pl'):
                currentLns -= 1
                f.close()
                break
            # Clean all
            elif shinput in ('.cleanall'):
                choice = input('Really? [Y/N] ')
                if choice.lower() == 'y':
                    fileLine = ['']
                    f.close()

                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(fileLine))
                        f.close()
                        break
            # Replace
            elif shinput in ('.replace', '.r'):
                target = input('Target? > ')
                replace = input('Replace? > ')

                fileLine[currentLns] = fileLine[currentLns].replace(target, replace)
                f.close()

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(fileLine))
                    f.close()
                    break
            # Writing
            else:
                fileLine[currentLns] = shinput
                f.close()

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(fileLine))
                    f.close()
                    break

if __name__ == "__main__":
    print("OmegaEdit dev commit-7th")
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <filename>")
    else:
        print(f"Editing {sys.argv[-1]} as ed advanced mode.")
        ed_mode(sys.argv[-1])
