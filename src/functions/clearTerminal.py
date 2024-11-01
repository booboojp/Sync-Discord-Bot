import os
from src.functions.terminalLog import terminal_log

async def clear_terminal():
    """
    Clears the terminal screen.

    This function attempts to clear the terminal screen using the appropriate command
    for the operating system. It logs the success or failure of the operation and ensures
    that a completion message is logged regardless of the outcome.

    Logs:
        SYSTEM: Terminal cleared.
        ERROR: Failed to clear terminal: <exception message>
        SYSTEM: clear_terminal function executed.

    Returns:
        None

    Raises:
        Exception: If an error occurs while attempting to clear the terminal.

    The function performs the following steps:
    1. Attempts to clear the terminal screen using 'cls' for Windows and 'clear' for Unix-based systems.
    2. Logs a message indicating that the terminal has been cleared.
    3. If an error occurs during the clearing process, logs an error message with the exception details.
    4. Logs a message indicating that the function execution is completed, regardless of success or failure.
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        await terminal_log("SYSTEM", "Terminal cleared.")
    except Exception as e:
        await terminal_log("ERROR", f"Failed to clear terminal: {e}")
    finally:
        await terminal_log("SYSTEM", "clear_terminal function executed.")

__all__ = ['clear_terminal']