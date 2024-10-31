import os
from src.functions.terminalLog import terminal_log

async def clear_terminal():
    """
    Clears the terminal screen.

    This function clears the terminal screen using the appropriate command
    for the operating system ('cls' for Windows, 'clear' for Unix-based systems).
    It also logs the action of clearing the terminal.

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    terminal_log("SYSTEM", "Terminal cleared.")

__all__ = ['clear_terminal']