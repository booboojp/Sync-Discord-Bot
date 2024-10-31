import json
from src.functions.terminalLog import terminal_log
__all__ = ['load_config']

def load_config():
    """
    Loads the configuration file.

    This function attempts to load the configuration file located at './src/settings/config.json'.
    It reads the JSON content of the file and returns it as a dictionary. The function logs the
    success or failure of the operation and raises exceptions if any errors occur during the process.

    Logs:
        CONFIG: Configuration file loaded.
        ERROR: Configuration file not found: <exception message>
        ERROR: Error decoding JSON from configuration file: <exception message>
        CONFIG: load_config function execution completed.

    Returns:
        dict: The configuration data loaded from the JSON file.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If there is an error decoding the JSON content of the file.

    The function performs the following steps:
    1. Attempts to open and read the configuration file.
    2. Logs a message indicating that the configuration file has been loaded.
    3. Returns the configuration data as a dictionary.
    4. If the file is not found, logs an error message and raises a FileNotFoundError.
    5. If there is an error decoding the JSON content, logs an error message and raises a JSONDecodeError.
    6. Logs a message indicating that the function execution is completed, regardless of success or failure.
    """
    try:
        with open("./src/settings/config.json", "r") as config_file:
            config = json.load(config_file)
        terminal_log("CONFIG", "Configuration file loaded.")
        return config
    except FileNotFoundError as e:
        terminal_log("ERROR", f"Configuration file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        terminal_log("ERROR", f"Error decoding JSON from configuration file: {e}")
        raise
    finally:
        terminal_log("CONFIG", "load_config function execution completed.")