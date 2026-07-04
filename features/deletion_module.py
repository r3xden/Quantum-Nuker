import discord
from typing import Optional

class DeletionModule:
    def __init__(self, bot_client: discord.Client):
        self.bot = bot_client

    async def delete_all_channels(self, guild_id: int) -> tuple[int, int]:
        """Deletes all channels in the given guild and returns deleted count/channel types."""
        print("\n--- STAGE 1/4: Deleting Channels & Categories ---")
        deleted_count = 0
        success_channels = []

        guild = self.bot.get_guild(guild_id)
        if not guild:
            print("Error: Could not find the specified Guild.")
            return 0, 0

        await guild.fetch_all_channels() # Ensure all are loaded if possible

        for channel in guild.channels:
            try:
                if isinstance(channel, discord.CategoryChannel):
                    await channel.delete(reason="Quantum Nuker Attack - Deleting Category")
                    print(f"✅ Deleted Category: {channel.name}")
                    deleted_count += 1
                    continue

                if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                    await channel.delete(reason="Quantum Nuker Attack - Deleting Channel")
                    print(f"✅ Deleted {type(channel).__name__}: {channel.name}")
                    deleted_count += 1
            except discord.Forbidden:
                print(f"❌ Could not delete {channel.name} (Permission Issue). Skipping.")
            except Exception as e:
                print(f"💥 Error deleting channel {channel.name}: {e}")

        return deleted_count, 0

    async def delete_roles(self, guild_id: int) -> int:
        """Deletes all roles in the given guild."""
        print("\n--- STAGE 2/4: Deleting Roles ---")
        deleted_count = 0
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return 0

        roles = [role for role in sorted(guild.roles, start=False, key=lambda r: r.position)]

        for i, role in enumerate(roles):
            if role.name == "Administrator" and len(roles) > 1:
                print("⚠️ Skipping Administrator role...")
                continue
            try:
                await role.delete(reason="Quantum Nuker Attack - Role Purge")
                print(f"✅ Deleted Role: {role.name} (ID: {role.id})")
                deleted_count += 1
            except discord.Forbidden:
                print(f"❌ Could not delete role {role.name} (Permission Issue). Skipping.")
            except Exception as e:
                print(f"💥 Error deleting role {role.name}: {e}")
        return deleted_count

    async def delete_webhooks(self, guild_id: int) -> int:
        """Deletes all webhooks."""
        print("\n--- STAGE 3/4: Deleting Webhooks ---")
        deleted_count = 0
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return 0

        webhooks = [hook async for hook in guild.sm.webhooks] # Use SM if available, otherwise direct fetch

        for webhook in webhooks:
            try:
                await webhook.delete(reason="Quantum Nuker Attack - Webhook Purge")
                print(f"✅ Deleted Webhook: {webhook.name}")
                deleted_count += 1
            except discord.Forbidden:
                print(f"❌ Could not delete webhook {webhook.name} (Permission Issue). Skipping.")
            except Exception as e:
                print(f"💥 Error deleting webhook {webhook.name}: {e}")

        return deleted_count
