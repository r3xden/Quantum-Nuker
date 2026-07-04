# Quantum Nuker - The Ultimate Discord Server Annihilator!

## Overview
The Quantum Nuker is a comprehensive, multi-stage asynchronous Python tool designed to completely dismantle a specified Discord server. It doesn't just kick people; it purges infrastructure, floods the system with garbage content, and leaves behind a chaotic, unusable mess.

**WARNING: This bot has no safety features beyond manual intervention and runs aggressively.**
Use this tool ONLY on servers you intend to wreck or on test environments!

---

# Features

The tool performs a continuous, no-mercy assault on the specified guild through four primary phases:
1. **Mass Ban:** Iteratively bans every member found in the server until forced to stop by permissions or rate limits.
2. **Mass Destruction:** Deletes all existing roles and systematically strips out text/voice channels, along with deleting associated webhooks.
3. **Mass Creation:** Rapidly spams the guild by creating a large volume of randomized spamming channels and roles using predefined keywords (e.g., "pussyeater", "fuckyou", etc.).
4. **Mass Ping Storm:** Continuously sends an overwhelming barrage of `@everyone` / `@here` pings into all relevant target channels, aiming for extreme message throughput (simulated up to 1k messages per 5 seconds burst).

---

# Tool Details & Installation

## Prerequisites

+ **Python Version:** 3.8+ is recommended.
+ **Library:** `discord.py` (Ensure you have installed dependencies listed in `requirements.txt`).
+ **Permissions:** The Bot Token must belong to a bot with **Administrator** permissions *at least* on the target server to ensure all functions work correctly.

## Setup and Execution

1 | **Clone repository:**
```bash
git clone https://github.com/r3xden/Quantum-Nuker
```

2 | **CD into repository:**
```bash
cd Quantum-Nuker
```

3 |  **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4 | **Run the tool:**
```bash
python main.py
```

---

# Usage Flow (CLI Interaction)

The script will guide you through the following steps sequentially:

- Enter your Bot Token.
- Enter the Target Guild ID.
- Confirm execution with yes or no.
- If confirmed, the attack starts in stages: Bloat Creation $\rightarrow$ Deletion $\rightarrow$ Ban $\rightarrow$ Spam Flood **(Continues until you manually stop it - exit the terminal best).**

---

# Development Notes & Advanced Customization

- **Spam Rate:** To adjust the ping rate, modify MESSAGE_DELAY_SECONDS in config.py. Lowering this value means faster spamming, up to Discord's API limits.
- **Bloat Names:** Customize the list of names/themes in config.py: RANDOM_NICKNAMES.
- **Bot Logic:** All primary attack steps are isolated into features/* modules for modular maintenance.

---

# Credits

This project was created by **Rexden**.
This code is provided strictly for Educational Purpose Only and should be used to learn about advanced asynchronous programming, rate limiting, and Discord API abuse techniques.
