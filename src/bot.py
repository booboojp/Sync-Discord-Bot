import discord
from discord.ext import commands
from src.functions.terminalLog import terminal_log
from src.functions.clearTerminal import clear_terminal
from src.functions.syncRoles import sync_roles
from src.functions.loadConfig import load_config

CONFIG = load_config()
TOKEN = CONFIG["token"]
VERSION = CONFIG["version"]
MAIN_SERVER_ID = CONFIG["main_server_id"]
SYNC_SERVER_ID = CONFIG["sync_server_id"]
ROLE_ID_MAP = {int(k): int(v) for k, v in CONFIG["role_id_map"].items()}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="s.", intents=intents)

@client.event
async def on_ready():
    """
    Event handler for when the bot is ready.

    This function is triggered when the bot has successfully connected to Discord and is ready to operate.
    It performs the following actions:
    1. Clears the terminal screen to provide a clean slate for logging.
    2. Sets the bot's status to online.
    3. Logs a message indicating that the bot has been loaded with its version.
    4. Logs a message indicating that the bot is now online with its user ID.

    Logs:
        BOT: Logs a message indicating that the bot has been loaded with its version.
        BOT: Logs a message indicating that the bot is now online with its user ID.

    Exceptions:
        Exception: Catches any exception that occurs during the terminal clearing process and logs an error message.

    The function performs the following steps:
    1. Calls the `clear_terminal` function to clear the terminal screen.
    2. Sets the bot's presence status to online using `client.change_presence`.
    3. Logs the bot's name and version using the `terminal_log` function.
    4. Logs the bot's name and user ID using the `terminal_log` function.
    """
    clear_terminal()
    await client.change_presence(status=discord.Status.online)
    terminal_log("BOT", f"{client.user.name} version {VERSION} loaded.")
    terminal_log("BOT", f"{client.user.name} ({client.user.id}) is now online.")

"""
Event handler for when a member's roles are updated in the main server.

This function is triggered whenever a member's roles are updated in the main server.
It checks if the roles have changed and if the update occurred in the main server.
If both conditions are met, it logs a message indicating that the roles have been synchronized
and calls the `sync_roles` function to synchronize the member's roles between the main server
and the sync server.

Args:
    before (discord.Member): The member object before the update.
    after (discord.Member): The member object after the update.

Logs:
    BOT: Logs a message indicating that the roles for the member have been synchronized in the main server.

Raises:
    Exception: If any error occurs during the role synchronization process.

The function performs the following steps:
1. Checks if the member's roles have changed and if the update occurred in the main server.
2. Logs a message indicating that the roles for the member have been synchronized in the main server.
3. Calls the `sync_roles` function to synchronize the member's roles between the main server and the sync server.
4. If an error occurs during the role synchronization process, logs an error message with the exception details.
"""
@client.event
async def on_member_update(before, after):
    if before.roles != after.roles and before.guild.id == MAIN_SERVER_ID:
        terminal_log("BOT", f"Synchronized roles for {before.name} as they updated in the Main Server.")
        await sync_roles(before.guild, client.get_guild(SYNC_SERVER_ID), before.id, ROLE_ID_MAP)
client.run(TOKEN)