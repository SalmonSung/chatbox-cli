import click
import asyncio
from colorama import Fore, Style, init
from .interface import print_human, print_ai, print_separator
# from chatbox.core.pipeline import *
from chatbox.core.graph_controller import *

init(autoreset=True)


@click.group()
def cli():
    """Chatbox CLI tool with multiple commands."""
    pass


@cli.command()
@click.option('--repeat', default=2, help='Number of chat turns (demo).')
def chat(repeat):
    """Start a chatbox session."""
    agent = AgentBuilder(save_history="disabled")
    print("Starting Chatbox Session!\n")
    for _ in range(repeat):
        is_done = False
        human_feedback = ""
        user_message = click.prompt(click.style("You (type a message)", fg="cyan"))
        print_human(user_message)
        if user_message == "q":
            print(f"{Fore.YELLOW}{Style.NORMAL}Session ended. Goodbye!")
            break
        results, is_done = asyncio.run(agent.run_graph(user_message))
        # print(f"Results: {results}, is_done: {is_done}")
        while not is_done:
            user_message = click.prompt(click.style(results, fg="cyan"))
            results, is_done = asyncio.run(agent.resume_graph(user_message))
            if is_done:
                print_ai(results)

            print_separator()

        # print_human(user_message)
        # ai_response = f"Echo: {user_message[::-1]}"
        # print_ai(ai_response)
    print(f"{Fore.YELLOW}{Style.NORMAL}Session ended. Goodbye!")


@cli.command()
def clean():
    """Clean conversation history."""
    # Here, you would clear your memory or history file.
    print(f"{Fore.RED}{Style.NORMAL}Conversation history cleaned!")


@cli.command()
def update():
    """Force chatbox to update its memory."""
    # Here, you would trigger a memory update routine.
    print(f"{Fore.GREEN}{Style.NORMAL}Conversation history cleaned!")


if __name__ == "__main__":
    cli()  # Not main(), but cli() for Click group!
