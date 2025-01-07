#!/bin/python3

import sys

def ed_mode(filename):
    while True:
        with open(filename, 'r', encoding='utf-8') as f:
            f.seek(0)  # Move cursor to the beginning of the file
            file = f.read()
            fileLine = file.split('\n')
            print("\n==================")
            print(filename)
            print("==================")
            for i in range(len(fileLine)):
                print(f"{i+1} | {fileLine[i]}")
            print("==================")
        currentLns = 0
        while True:
            shinput = input(f'[Ln {currentLns+1}] > ')
            if shinput == '.nextline':
                currentLns += 1
                fileLine.append('')
                pass
            
            elif shinput == '.prevline':
                currentLns -= 1
            else:
                fileLine[currentLns] = shinput
                f.close()

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(fileLine))
                    f.close()
                    break

if __name__ == "__main__":
    print("OmegaEdit alpha-0")
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <filename>")
    else:
        print(f"Editing {sys.argv[-1]} as ed advanced mode.")
        ed_mode(sys.argv[-1])
