import discord
from typing import TYPE_CHECKING
from config import SPAM_CHANNEL_NAMES, NUM_TO_CREATE_DEFAULT

if TYPE_CHECKING:
    from bot_handler import BotHandler

class SpamGenerator:
    def __init__(self, client) -> None:
        self.client = client
        pass 

    async def mass_create_channels(self, guild_id: int, bot_handler: 'BotHandler', stop_event):
        """Continuously creates spam channels until the stop_event is set."""
        print("\n[STATUS] --- Initiating Mass Channel Generation Spam... ---")
        created_count = 0

        try:
            guild = self.client.get_guild(guild_id)
            if not guild:
                 print("Error: Could not get guild object.")
                 return

            spam_roles = []
            for i in range(1, 5):
                role = await guild.create_role(name=f"SpamRole{i}", color=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                spam_roles.append(role)

        except Exception as e:
            print(f"[FATAL] Failed to setup initial roles: {e}")


        while not stop_event.is_set():
            channel_name = SPAM_CHANNEL_NAMES[created_count % len(SPAM_CHANNEL_NAMES)]

            try:
                new_channel = await self.client.get_guild(guild_id).create_text_channel(
                    name=channel_name, 
                    topic=f"Spam spamspamspam {NUKER_CREDIT} effect.",
                    reason="Automated Nuke Cycle"
                )
                print(f"[SPAM] Successfully created channel: #{new_channel.name}")
                created_count += 1

            except discord.Forbidden:
                print("[WARN] Could not create spam channel - Permissions insufficient.")
                break
            except Exception as e:
                print(f"[ERROR] Failed to create channel {channel_name}: {e}")
                await self.client.sleep(10) 

            await self.client.sleep(0.5)

        print(f"\n[STOP] Spam generation finished. Total channels created (approx): {created_count}")

import random
