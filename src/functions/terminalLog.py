import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H.%M.%d'
)

__all__ = ['terminal_log']

async def terminal_log(prefix, message):
    """
    Logs a message to the terminal and handles any exceptions that occur during the logging process.

    This function attempts to log a message with a given prefix using the logging module. If an exception occurs
    during the logging process, it catches the exception and prints an error message to the terminal. Regardless
    of whether an exception occurs, it ensures that a completion message is printed to the terminal.

    Args:
        prefix (str): A string prefix to categorize the log message (e.g., "ERROR", "SYSTEM", "BOT").
        message (str): The message to be logged.

    Logs:
        INFO: Logs the message with the given prefix.
        ERROR: If an exception occurs, logs an error message with the exception details.
        SYSTEM: Logs a completion message indicating that the function execution is completed.

    Exceptions:
        Exception: Catches any exception that occurs during the logging process and prints an error message.

    The function performs the following steps:
    1. Attempts to log the message with the given prefix using the logging module.
    2. If an exception occurs, catches the exception and prints an error message with the exception details.
    """
    try:
        logging.info(f'[{prefix}] {message}')
    except Exception as e:
        print(f'[{prefix}] An error occurred: {e}')