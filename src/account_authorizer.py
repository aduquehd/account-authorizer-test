# Validators
from dataclasses import dataclass

# Utils
from src.utils.account import Account

# Handlers
from src.handlers.account_handler import initialize_account
from src.handlers.event_handler import get_event_list_from_stdin
from src.handlers.operations_handler import process_events


def _print_results(event_result):
    """
    Print the results on the console
    :param event_result: List, event results.
    """
    for event in event_result:
        print(event)


def main():
    """
    Execute the application.
    """
    event_list = get_event_list_from_stdin()
    # account = initialize_account()
    event_result = process_events(event_list=event_list)
    _print_results(event_result)
