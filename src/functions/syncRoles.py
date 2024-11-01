import discord
from src.functions.terminalLog import terminal_log

__all__ = ['sync_roles']

async def sync_roles(main_server, sync_server, user_id, role_id_map):
    """
    Synchronizes roles for a user between the main server and the sync server.
    This function retrieves the user from both the main server and the sync server,
    removes any roles in the sync server that are mapped in the role_id_map, and then
    adds roles to the user in the sync server based on their roles in the main server.
    Args:
        main_server (discord.Guild): The main server object where the user's roles are sourced.
        sync_server (discord.Guild): The sync server object where the user's roles are synchronized.
        user_id (int): The ID of the user whose roles are being synchronized.
        role_id_map (dict): A dictionary mapping role IDs from the main server to the sync server.
    Returns:
        None
    Logs:
        "DEBUG": If the user is not found in either the main server or the sync server.
        "BOT": When roles are successfully cleared or added in the sync server.
        "ERROR": If there are missing permissions to remove or add roles, or if any other error occurs during synchronization.
        "DEBUG": When the role synchronization process is completed.
    Raises:
        Exception: If any error occurs during the role synchronization process.
    The function performs the following steps:
    1. Retrieves the user from both the main server and the sync server.
    2. Logs a debug message if the user is not found in either server.
    3. Identifies roles in the sync server that need to be removed based on the role_id_map.
    4. Attempts to remove the identified roles from the user in the sync server.
    5. Logs a message if roles are successfully removed or if there are missing permissions.
    6. If the user is found in the main server, retrieves their roles.
    7. Maps the user's roles from the main server to the sync server using the role_id_map.
    8. Attempts to add the mapped roles to the user in the sync server.
    9. Logs a message if roles are successfully added or if there are missing permissions.
    10. Logs a debug message when the role synchronization process is completed.
    """
    try:
        main_member = main_server.get_member(user_id)
        sync_member = sync_server.get_member(user_id)

        if main_member is None:
            await terminal_log("DEBUG", f"User with ID {user_id} not found in Main Server.")
        if sync_member is None:
            await terminal_log("DEBUG", f"User with ID {user_id} not found in Sync Server.")
            return

        sync_roles_to_remove = [role for role in sync_member.roles if role.id in role_id_map.values()]

        if sync_roles_to_remove:
            try:
                await sync_member.remove_roles(*sync_roles_to_remove, reason="Removing sync roles.")
                await terminal_log("BOT", f"Cleared sync roles for {sync_member.name} in the Sync Server.")
            except discord.errors.Forbidden:
                await terminal_log("ERROR", f"Missing permissions to remove roles from {sync_member.name} in the Sync Server.")

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
                        await terminal_log("BOT", f"Gave {sync_member.name} the role {sync_role.name} in the Sync Server.")
                    except discord.errors.Forbidden:
                        await terminal_log("ERROR", f"Missing permissions to add roles to {sync_member.name} in the Sync Server.")
    except Exception as e:
        await terminal_log("ERROR", f"An error occurred during role synchronization: {e}")
    finally:
        await terminal_log("DEBUG", "Role synchronization process completed.")
