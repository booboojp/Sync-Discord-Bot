import json
from src.functions.terminalLog import terminal_log
__all__ = ['load_config']

def load_config():
    """
    Loads the configuration from a JSON file.

    This function opens the configuration file located at './src/settings/config.json',
    reads its contents, and parses it as a JSON object. It also logs a message indicating
    that the configuration file has been loaded.

    Returns:
        dict: The parsed JSON configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    with open("./src/settings/config.json", "r") as config_file:
        config = json.load(config_file)
    terminal_log("CONFIG", "Configuration file loaded.")
    return config