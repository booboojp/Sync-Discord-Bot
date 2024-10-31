import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H.%M.%d'
)

__all__ = ['terminal_log']

async def terminal_log(prefix, message):
    """
    Logs a message with a given prefix to the terminal.

    Args:
        prefix (str): The prefix to be added to the log message.
        message (str): The message to be logged.

    Returns:
        None
    """
    logging.info(f'[{prefix}] {message}')