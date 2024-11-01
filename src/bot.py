import sys
import os
import json
import discord
from discord.ext import commands
from src.functions.terminalLog import terminal_log
from src.functions.clearTerminal import clear_terminal
from src.functions.syncRoles import sync_roles
from src.functions.loadConfig import load_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def main():
    with open("./src/settings/config.json", "r") as config_file:
        CONFIG = json.load(config_file)
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
        await clear_terminal()
        await client.change_presence(status=discord.Status.online)
        await terminal_log("BOT", f"{client.user.name} version {VERSION} loaded.")
        await terminal_log("BOT", f"{client.user.name} ({client.user.id}) is now online.")

    @client.event
    async def on_member_update(before, after):
        if before.roles != after.roles and before.guild.id == MAIN_SERVER_ID:
            await terminal_log("BOT", f"Synchronized roles for {before.name} as they updated in the Main Server.")
            await sync_roles(before.guild, client.get_guild(SYNC_SERVER_ID), before.id, ROLE_ID_MAP)

    await client.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())