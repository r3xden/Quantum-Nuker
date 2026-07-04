import discord
from typing import TYPE_CHECKING
from config import PING_MESSAGE, MESSAGES_PER_BATCH, PING_INTERVAL_SECONDS

if TYPE_CHECKING:
    from bot_handler import BotHandler

class PingEngine:
    def __init__(self, client) -> None:
        self.client = client

    async def mass_ping(self, guild_id: int):
        """Sends massive pings to the specified channels."""
        print("\n[STATUS] --- Initiating High-Velocity Mass Ping Sequence... ---")
        try:
            guild = self.client.get_guild(guild_id)
            if not guild:
                print("Error: Could not retrieve target guild.")
                return
              
            pings_sent = 0

            while True:
                try:
                    print(f"\n[PING] Sending burst of {MESSAGES_PER_BATCH} messages...")

                    tasks = []
                    ping_message = PING_MESSAGE

                    await guild.get_channel(guild.get_channel(1).id if guild.get_channel(1) else None).send(ping_message)
                    print("    -> Pinned to default channels.")
                    pings_sent += 1

                    print("    -> Pushing through high-frequency message bursts...")
                    await self._burst_send(guild, ping_message)

                except discord.Forbidden:
                    print("[ERROR] Ping failed: Bot lacks necessary permissions.")
                    break
                except Exception as e:
                    print(f"[FATAL ERROR IN PING ENGINE]: {e}")
                    break

                await self.client.sleep(PING_INTERVAL_SECONDS)

        except Exception as e:
             print(f"[ERROR] General error during pinging process: {e}")


    async def _burst_send(self, guild: discord.Guild, message: str):
        """Helper function to spam multiple messages rapidly."""
        tasks = []
        target_channels = [channel for channel in guild.text_channels if channel]

        if not target_channels:
            print("    [WARN] No text channels found to spam ping.")
            return

        for i, channel in enumerate(target_channels):
             try:
                 await channel.send(f"Burst Ping {i+1}/{len(target_channels)}: {message}")
             except discord.Forbidden:
                pass

        print(f"[SUCCESS] Attempted to ping across all available channels.")
