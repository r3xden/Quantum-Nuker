import discord
from typing import List

# --- Constants ---
TOOL_NAME = "Quantum Nuker"
DESCRIPTION = "Automated Discord Server Annihilation Tool."
OWNER_CREDITS = "Rexden"
DEFAULT_PING_MESSAGE = "@everyone and @here\nHahaha! Nuked by Quantum Nuker, Created by Rexden - https://github.com/r3xden"

# --- Helper Functions ---

def get_admin_permissions(guild: discord.Guild) -> bool:
    """Checks if the bot has all necessary administrative permissions."""
    if not guild:
        return False

    try:
        # We check against the guild itself, assuming the bot client has context.
        channel = discord.utils.get(guild.text_channels, type=discord.Channel)
        if channel:
            # For broader check, we just ensure the required scope is present
            return bool(getattr(bot.user, 'guild_permissions', None) and 
                            hasattr(bot.user.guild_permissions, 'administrator') and 
                            bot.user.guild_permissions.administrator)
        return True # Fallback if channel check fails, relies on client setup
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return False

def create_status_message(action: str, success: bool = True) -> str:
    """Generates formatted status messages."""
    status = "SUCCESS" if success else "FAILURE"
    return f"\n[{status}]: {action}"
