
def clear_screen():
    """Clear the entire screen and move the cursor to the top-left corner."""
    print("\033[2J\033[H", end="")

def clear_line():
    """Clear the current line."""
    print("\033[2K", end="")

if __name__ == "__main__":
    