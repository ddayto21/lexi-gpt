# app/clients/llm_repl.py

import argparse
import asyncio
import sys
import os
from dotenv import load_dotenv
from app.clients.llm_client import DeepSeekAPIClient
from colorama import init, Fore, Style
import readline  # For better input handling and keyboard shortcuts

# Initialize colorama for cross-platform colored terminal output.
init(autoreset=True)


# -----------------------------------------------------------------------------
# Helper function to read a multi-line prompt.
# The user can type multiple lines. When finished, they type '/send' on a new line.
# -----------------------------------------------------------------------------
def read_multiline_prompt() -> str:
    """
    Read multi-line input from the user until '/send' is entered on a new line.
    Returns:
        The full prompt as a single string.
    """
    print(Fore.CYAN + "Enter your prompt (type '/send' on a new line when finished):")
    lines = []
    while True:
        try:
            line = input(Fore.YELLOW + "> ")
            # When user types '/send', end the input collection.
            if line.strip() == "/send":
                break
            lines.append(line)
        except KeyboardInterrupt:
            print(
                Fore.RED
                + "\nInput interrupted. Use '/send' to finish or 'quit' to exit."
            )
    return "\n".join(lines)


async def main():
    # Load environment variables from .env file.
    load_dotenv()

    # Setup command-line argument parser.
    parser = argparse.ArgumentParser(description="DeepSeek CLI Client")
    parser.add_argument(
        "--model",
        type=str,
        default="deepseek-chat",
        help="Model to use (default: deepseek-chat)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature parameter (default: 0.7)",
    )
    parser.add_argument(
        "--async-mode",
        action="store_true",
        help="Use asynchronous streaming",
    )
    args = parser.parse_args()

    # Create an instance of the DeepSeekAPIClient.
    client = DeepSeekAPIClient(api_key=os.getenv("DEEPSEEK_API_KEY"))

    # Display token balance.
    token_balance = client.get_token_balance()
    print(Fore.GREEN + Style.BRIGHT + f"Token Balance: {token_balance}\n")

    # Display task selection menu.
    print(
        Fore.CYAN + Style.BRIGHT + "Select a task by entering the corresponding number:"
    )
    print(Fore.YELLOW + "1: Coding (Temperature: 0.0)")
    print(Fore.YELLOW + "2: Data Cleaning (Temperature: 1.0)")
    print(Fore.YELLOW + "3: General Conversation / Translation (Temperature: 1.3)")
    print(Fore.YELLOW + "4: Creative Writing (Temperature: 1.5)")
    task_choice = input(Fore.CYAN + "Your choice (1-4): ").strip()

    # Set temperature based on the task choice.
    temperature_map = {
        "1": 0.0,
        "2": 1.0,
        "3": 1.3,
        "4": 1.5,
    }
    args.temperature = temperature_map.get(task_choice, 0.7)
    print(Fore.GREEN + f"Temperature set to {args.temperature}.\n")

    # Interactive REPL loop.
    while True:
        try:
            # Read multi-line user prompt.
            prompt = read_multiline_prompt()
            if prompt.strip().lower() == "quit":
                print(Fore.MAGENTA + "\nExiting interactive session.")
                break

            # Build the message(s) to send to the API.
            messages = [{"role": "user", "content": prompt}]

            print(Fore.CYAN + "\n--- Answer ---")
            if args.async_mode:
                async for chunk in client.async_stream(
                    model=args.model,
                    messages=messages,
                    temperature=args.temperature,
                ):
                    print(chunk, end="", flush=True)
                print(Fore.CYAN + "\n--------------\n")
            else:
                for chunk in client.sync_stream(
                    model=args.model,
                    messages=messages,
                    temperature=args.temperature,
                ):
                    print(chunk, end="", flush=True)
                print(Fore.CYAN + "\n--------------\n")

        except KeyboardInterrupt:
            print(
                Fore.RED
                + "\nOperation interrupted by user. Type 'quit' to exit or continue."
            )


# python -m app.clients.llm_reply --model deepseek-chat
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\nOperation interrupted by user.")
        sys.exit(0)
