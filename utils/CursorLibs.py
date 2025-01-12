
def clear_screen():
    """Clear the entire screen and move the cursor to the top-left corner."""
    print("\033[2J\033[H", end="")

def clear_line():
    """Clear the current line."""
    print("\033[2K", end="")
if __name__ == "__main__":
    # 输出带有白色背景的字符串
    print("\033[47mThis is a string with a white background.\033[0m")
