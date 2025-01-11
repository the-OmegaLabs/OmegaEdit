#!/bin/python3

import sys
import os
import utils.CursorLibs as Curs
import colorama
import fcntl

colorama.init()

def printAll(fileLine, currentLns):
    print("==================")
    for i in range(len(fileLine)):
        if i == currentLns:
            currentSign = f'{colorama.Style.BRIGHT}|{colorama.Style.RESET_ALL}'
        else:
            currentSign = '|'
        lineString = f"{i + 1:>{len(str(len(fileLine)))}}"  # 行号对齐优化
        print(f"{lineString} {currentSign} {fileLine[i]}")
    print("==================")

def write(filename, fileLine):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fileLine))
        f.close()

def lock_file(file):
    try:
        fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except IOError:
        print("File is already locked by another process.")
        return False

def ed_mode(filename):
    print("HINT: type .help to open help menu")
    print("      You can exit the editor with .quit/.q command.")
    
    currentLns = 0
    toggleDisplay = True
    toggleClean = True
    toggleAppend = True
    history = []

    # 文件检查与初始化
    if not os.path.exists(filename):
        open(filename, 'w', encoding='utf-8').close()

    # 打开文件并检查锁
    with open(filename, 'r+', encoding='utf-8') as f:
        if not lock_file(f):
            return

    while True:
        # 读取文件内容
        with open(filename, 'r', encoding='utf-8') as f:
            f.seek(0)
            file = f.read()
            fileLine = file.split('\n')

        print(f"Editing {filename}")

        if toggleDisplay:
            printAll(fileLine, currentLns)

        try:
            shinput = input(f'I {currentLns + 1} > ')
        except KeyboardInterrupt:
            exit()

        # 命令逻辑
        if shinput in ('.nextline', '.n'):
            if currentLns + 1 < len(fileLine):
                currentLns += 1
            else:
                fileLine.append('')
                currentLns = len(fileLine) - 1

        elif shinput.startswith('.goto') or shinput.startswith('.g'):
            gotoLns = int(shinput.split(' ')[-1]) - 1
            if 0 <= gotoLns < len(fileLine):
                currentLns = gotoLns

        elif shinput in ('.append', '.ta'):
            toggleAppend = not toggleAppend
            print("Append mode:", "Enabled" if toggleAppend else "Disabled")

        elif shinput in ('.display', '.td'):
            toggleDisplay = not toggleDisplay
            print("File display:", "Enabled" if toggleDisplay else "Disabled")

        elif shinput in ('.prevline', '.p'):
            if currentLns > 0:
                currentLns -= 1

        elif shinput in ('.cleanall', '.ca'):
            choice = input('Really clean all lines? [Y/N] ')
            if choice.lower() == 'y':
                history.append(fileLine[:])  # 保存快照
                fileLine = ['']
                currentLns = 0

        elif shinput in ('.cleanline', '.cl'):
            choice = input(f'Really clean line {currentLns + 1}? [Y/N] ')
            if choice.lower() == 'y':
                history.append(fileLine[:])  # 保存快照
                fileLine[currentLns] = ''

        elif shinput in ('.quit', '.q'):
            f.close()
            write(filename, fileLine)
            break

        elif shinput in ('.autoclean', '.tc'):
            toggleClean = not toggleClean
            print("Auto clean screen:", "Enabled" if toggleClean else "Disabled")

        elif shinput in ('.help', '.h'):
            print("""
    .help      (.h)  - Show this help menu
    .goto      (.g)  - Go to a specific line
    .nextline  (.n)  - Move to the next line
    .prevline  (.p)  - Move to the previous line
    .replace   (.r)  - Replace text on the current line
    .duplicate (.d)  - Duplicate the current line
    .quit      (.q)  - Quit the editor
    .cleanall  (.ca) - Clear all lines
    .cleanline (.cl) - Clear the current line
    .display   (.td) - Toggle file display
    .append    (.ta) - Toggle append mode
    .autoclean (.tc) - Toggle auto clean screen
    .undo      (.u)  - Undo the last action
            """)

        elif shinput in ('.duplicate', '.d'):
            history.append(fileLine[:])  # 保存快照
            fileLine.insert(currentLns + 1, fileLine[currentLns])
            currentLns += 1

        elif shinput in ('.replace', '.r'):
            target = input('Target? ').strip()
            if not target:
                print("Target cannot be empty.")
                continue
            replace = input('Replace as? ').strip()
            history.append(fileLine[:])  # 保存快照
            fileLine[currentLns] = fileLine[currentLns].replace(target, replace)

        elif shinput in ('.undo', '.u'):
            if history:
                fileLine = history.pop()
                print("Undo successful.")
            else:
                print("No actions to undo.")

        else:
            history.append(fileLine[:])  # 保存快照
            if toggleAppend:
                fileLine[currentLns] += shinput
            else:
                fileLine[currentLns] = shinput

        if toggleClean:
            Curs.clear_screen()

        f.close()
        write(filename, fileLine)

if __name__ == "__main__":
    print("\nOmegaEdit 0.1")
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <filename>")
    else:
        ed_mode(sys.argv[-1])
