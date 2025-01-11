def move_up(lines=1):
    """Move the cursor up by the specified number of lines."""
    print(f"\033[{lines}A", end="")

def move_down(lines=1):
    """Move the cursor down by the specified number of lines."""
    print(f"\033[{lines}B", end="")

def move_right(columns=1):
    """Move the cursor right by the specified number of columns."""
    print(f"\033[{columns}C", end="")

def move_left(columns=1):
    """Move the cursor left by the specified number of columns."""
    print(f"\033[{columns}D", end="")

def set_position(row, column):
    """Set the cursor position to the specified row and column."""
    print(f"\033[{row};{column}H", end="")

def save_position():
    """Save the current cursor position."""
    print("\033[s", end="")

def restore_position():
    """Restore the cursor to the last saved position."""
    print("\033[u", end="")

def hide_cursor():
    """Hide the cursor."""
    print("\033[?25l", end="")

def show_cursor():
    """Show the cursor."""
    print("\033[?25h", end="")

def clear_screen():
    """Clear the entire screen and move the cursor to the top-left corner."""
    print("\033[2J\033[H", end="")

def clear_line():
    """Clear the current line."""
    print("\033[2K", end="")