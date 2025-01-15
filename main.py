import sys
import os
import utils.CursorLibs as Curs
import colorama

colorama.init()

def create_fill_char():
    return "=" * os.get_terminal_size().columns

def printAll(fileLine, currentLns, sectionColA: int, sectionColB: int, hint=None):
    fill_char = create_fill_char()
    if hint:
        print(hint)
    print(fill_char)
    width = len(str(len(fileLine)))
    for i, line in enumerate(fileLine):
        if not sectionColA is None:
            if sectionColB is not None and sectionColB >= 0:
                line = line[:sectionColA] + colorama.Back.WHITE + colorama.Fore.BLACK + line[sectionColA:sectionColB] + colorama.Fore.RESET + colorama.Back.RESET + line[sectionColB:]
        currentSign = f'{colorama.Style.BRIGHT}|{colorama.Style.RESET_ALL}' if i == currentLns else '|'
        print(f"{i + 1:>{width}} {currentSign} {line}")
    print(fill_char)

def write(filename, fileLine):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fileLine))
    except Exception as e:
        print(f"Error writing to file: {e}")

def handle_resize(signum, frame):
    global fill_char
    fill_char = create_fill_char()

def ed_mode(filename):
    global use_autoresize, cursor_mode
    print("HINT: type .help to open the help menu")
    print("      You can exit the editor with .quit/.q command.")

    currentLns = 0
    toggleDisplay = True
    toggleClean = True
    toggleAppend = True
    history = []
    selection = None
    clipboard = None
    customHint = None
    sectionColA = None
    sectionColB = None

    if not os.path.exists(filename):
        try:
            open(filename, 'w', encoding='utf-8').close()
        except Exception as e:
            print(f"Error creating file: {e}")
            return


    while True:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                fileLine = f.read().split('\n')
        except Exception as e:
            print(f"Error reading file: {e}")
            break

        if toggleDisplay:
            print(f"Editing {filename}")
            printAll(fileLine, currentLns, sectionColA, sectionColB, customHint)
            customHint = None

        try:
            shinput = input(f'I {currentLns + 1} > ')
        except KeyboardInterrupt:
            print("\nExiting... Goodbye!")
            break
        except EOFError:
            print("\nInput error detected. Exiting...")
            break

        if shinput.startswith(':'):
            pass

        else:
            if shinput in ('.nextline', '.n'):
                currentLns = min(currentLns + 1, len(fileLine) - 1)

            elif shinput.startswith(('.goto', '.g')):
                try:
                    gotoLns = int(shinput.split(' ')[-1]) - 1
                    if 0 <= gotoLns < len(fileLine):
                        currentLns = gotoLns
                    else:
                        print("Line number out of range.")
                except ValueError:
                    print("Invalid line number.")

            elif shinput in ('.append', '.ta'):
                toggleAppend = not toggleAppend

            elif shinput in ('.display', '.td'):
                toggleDisplay = not toggleDisplay

            elif shinput in ('.prevline', '.p'):
                currentLns = max(currentLns - 1, 0)

            elif shinput in ('.cleanall', '.ca'):
                if input('Really clean all lines? [Y/N] ').lower() == 'y':
                    history.append((fileLine[:], currentLns))
                    fileLine = ['']
                    currentLns = 0

            elif shinput in ('.cleanline', '.cl'):
                if input(f'Really clean line {currentLns + 1}? [Y/N] ').lower() == 'y':
                    history.append((fileLine[:], currentLns))
                    fileLine[currentLns] = ''

            elif shinput in ('.quit', '.q'):
                write(filename, fileLine)
                break

            elif shinput in ('.autoclean', '.tc'):
                toggleClean = not toggleClean

            elif shinput in ('.help', '.h'):
                input("""
        .help       (.h)  - Show this help menu
        .quit       (.q)  - Quit the editor
        .goto       (.g)  - Go to a specific line
        .nextline   (.n)  - Move to the next line
        .prevline   (.p)  - Move to the previous line
        .replace    (.r)  - Replace text on the current line
        .insert     (.i)  - Insert text at a specific column in the current line
        .duplicate  (.d)  - Duplicate the current line
        .undo       (.u)  - Undo the last action
        .cleanall   (.ca) - Clear all lines
        .cleanline  (.cl) - Clear the current line
        .display    (.td) - Toggle file display
        .append     (.ta) - Toggle append mode
        .autoclean  (.tc) - Toggle auto clean screen
        .select    (.sel) - Select texts
    """)

            elif shinput.startswith('.sel '):
                args = shinput.split(' ')
                try:
                    sectionColA = int(args[-2])
                    sectionColB = int(args[-1])
                except ValueError:
                    customHint = "Invalid column number.(1"
                    sectionColA = 0
                    sectionColB = None
                except IndexError:
                    customHint =  "Invalid column number.(2"
                    sectionColA = 0
                    sectionColB = None

            elif shinput.startswith('.unsel'):
                sectionColA = None
                sectionColB = None
    


            elif shinput.startswith('.insert '):
                try:
                    parts = shinput.split(' ', 2)  # Split into 3 parts: command, column, text
                    if len(parts) < 3:
                        raise ValueError("Missing arguments.")

                    _, insCol, insText = parts
                    insCol = int(insCol)

                    if insCol < 0 or insCol > len(fileLine[currentLns]):
                        raise IndexError("Column out of bounds.")

                    fileLine[currentLns] = fileLine[currentLns][:insCol] + insText + fileLine[currentLns][insCol:]
                    print("Text inserted successfully.")
                except ValueError as e:
                    print(f"Invalid syntax or input: {e}. Use: .insert <column> <text>")
                except IndexError as e:
                    print(f"Error: {e}")

            elif shinput in ('.duplicate', '.d'):
                history.append((fileLine[:], currentLns))
                fileLine.insert(currentLns + 1, fileLine[currentLns])
                currentLns += 1

            elif shinput.startswith('.replace '):
                try:
                    _, target, replace = shinput.split(' ', 2)
                    history.append((fileLine[:], currentLns))
                    fileLine[currentLns] = fileLine[currentLns].replace(target, replace)
                except ValueError:
                    print("Invalid syntax. Use: .replace <target> <replacement>")

            elif shinput in ('.undo', '.u'):
                if history:
                    fileLine, currentLns = history.pop()
                else:
                    print("No actions to undo.")

            elif shinput in ('.cursor', '.cur'):
                if cursor_mode:
                    cursor_mode = False
                    customHint = "Disabled cursor mode"
                else:
                    cursor_mode = True
                    customHint = "Disabled cursor mode"
            else:
                history.append((fileLine[:], currentLns))
                fileLine[currentLns] = fileLine[currentLns] + shinput if toggleAppend else shinput

        if toggleClean:
            Curs.clear_screen()

        write(filename, fileLine)

if __name__ == "__main__":
    print("\nOmegaEdit 0.1")
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <filename>")
    else:
        use_autoresize = True
        cursor_mode = False
        ed_mode(sys.argv[-1])
