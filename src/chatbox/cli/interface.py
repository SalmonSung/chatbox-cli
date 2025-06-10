# src/chatbox/cli/interface.py

from colorama import Fore, Style, init

init(autoreset=True)


def print_human(message):
    print(f"{Fore.CYAN}{Style.BRIGHT}[Human]: {message}")
    # print(f"{Fore.CYAN}{Style.BRIGHT}[Human]: {message}{Style.RESET_ALL}")


def print_ai(message):
    # print(f"{Fore.GREEN}{Style.BRIGHT}[AI]: {message}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}[AI]: {message}")


def print_separator():
    # print(f"{Fore.YELLOW}{'=' * 40}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 40}")