import discord
from src.functions.terminalLog import terminal_log

__all__ = ['sync_roles']

async def sync_roles(main_server, sync_server, user_id, role_id_map):
    """
    Synchronizes roles between a main server and a sync server for a specific user.
    Args:
        main_server (discord.Guild): The main server where the user's roles are sourced from.
        sync_server (discord.Guild): The sync server where the user's roles are to be synchronized.
        user_id (int): The ID of the user whose roles are being synchronized.
        role_id_map (dict): A mapping of role IDs from the main server to the sync server.
    Returns:
        None
    Logs:
        Logs various messages to the terminal_log function, including debug information, 
        success messages, and error messages related to permission issues.
    Raises:
        discord.errors.Forbidden: If the bot lacks permissions to add or remove roles in the sync server.
    """
    main_member = main_server.get_member(user_id)
    sync_member = sync_server.get_member(user_id)

    if main_member is None:
        terminal_log("DEBUG", f"User with ID {user_id} not found in Main Server.")
    if sync_member is None:
        terminal_log("DEBUG", f"User with ID {user_id} not found in Sync Server.")
        return

    sync_roles_to_remove = [role for role in sync_member.roles if role.id in role_id_map.values()]

    if sync_roles_to_remove:
        try:
            await sync_member.remove_roles(*sync_roles_to_remove, reason="Removing sync roles.")
            terminal_log("BOT", f"Cleared sync roles for {sync_member.name} in the Sync Server.")
        except discord.errors.Forbidden:
            terminal_log("ERROR", f"Missing permissions to remove roles from {sync_member.name} in the Sync Server.")

    if main_member is None:
        return
    
    main_user_roles = [role.id for role in main_member.roles]
    sync_user_roles = [role.id for role in sync_member.roles]

    for role_id in main_user_roles:
        sync_role_id = role_id_map.get(role_id)
        if sync_role_id:
            sync_role = sync_server.get_role(sync_role_id)
            if sync_role:
                try:
                    await sync_member.add_roles(sync_role, reason="Syncing roles from the main server.")
                    terminal_log("BOT", f"Gave {sync_member.name} the role {sync_role.name} in the Sync Server.")
                except discord.errors.Forbidden:
                    terminal_log("ERROR", f"Missing permissions to add roles to {sync_member.name} in the Sync Server.")
