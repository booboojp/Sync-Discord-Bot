import discord
from discord.ext import commands
import logging
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H.%M.%d'
)

with open("./src/settings/config.json", "r") as config_file:
    config = json.load(config_file)

def terminal_log(prefix, message):
    logging.info(f'[{prefix}] {message}')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

TOKEN = config["token"]
VERSION = config["version"]
MAIN_SERVER_ID = config["main_server_id"]
SYNC_SERVER_ID = config["sync_server_id"]
role_id_map = {int(k): int(v) for k, v in config["role_id_map"].items()}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix="s.", intents=intents)

@client.event
async def on_ready():
    clear_terminal()
    await client.change_presence(status=discord.Status.online)
    terminal_log("BOT", f"{client.user.name} version {VERSION} loaded.")
    terminal_log("BOT", f"{client.user.name} ({client.user.id}) is now online.")

@client.event
async def on_member_update(before, after):
    if before.roles != after.roles and before.guild.id == MAIN_SERVER_ID:
        print(f"[>] Synchronized roles for {before.name} as they updated in the Main Server.")
        await sync_roles(before.guild, client.get_guild(SYNC_SERVER_ID), before.id)

async def sync_roles(main_server, sync_server, user_id):
    main_member = main_server.get_member(user_id)
    sync_member = sync_server.get_member(user_id)

    if main_member is None:
        print(f"[D] User with ID {user_id} not found in Main Server.")
    if sync_member is None:
        print(f"[D] User with ID {user_id} not found in Sync Server")
        return

    sync_roles_to_remove = [role for role in sync_member.roles if role.id in role_id_map.values()]

    # Remove sync roles from the user on the sync server
    if sync_roles_to_remove:
        try:
            await sync_member.remove_roles(*sync_roles_to_remove, reason="Removing sync roles.")
            print(f"[-] Cleared sync roles the role for {sync_member.name} in the Sync Server.")
        except discord.errors.Forbidden:
            print(f"[!] Missing permissions to remove roles from {sync_member.name} in the Sync Server.")

    # Return after role clear if not on main server
    if main_member is None:
        return
    
    main_user_roles = [role.id for role in main_member.roles]
    sync_user_roles = [role.id for role in sync_member.roles]

    # Add roles on the sync server that the user has on the main server
    for role_id in main_user_roles:
        sync_role_id = role_id_map.get(role_id)
        if sync_role_id:
            sync_role = sync_server.get_role(sync_role_id)
            if sync_role:
                try:
                    await sync_member.add_roles(sync_role, reason="Syncing roles from the main server.")
                    print(f"[+] Gave {sync_member.name} the role {sync_role.name} in the Sync Server.")
                except discord.errors.Forbidden:
                    print(f"[!] Missing permissions to add roles to {sync_member.name} in the Sync Server.")

client.run(TOKEN)