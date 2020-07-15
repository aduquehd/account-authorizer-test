from src.utils.account import Account


def initialize_account():
    """
    Initialize account when application start.
    :return: Object, Account object defined on utils.
    """
    return Account(
        is_active_card=False,
        available_limit=0,
        is_initialized=False,
        is_premium=False,
    )


def new_account(is_active_card, available_limit, is_initialized=True, is_premium=False):
    """
    Return new account
    :param is_active_card: Bool, is active card param. e.g. True or False.
    :param available_limit: Float, new available limit. e.g. 500.
    :param is_initialized: Bool, is the account initialized. e.g. True or False.
    :param is_premium: Bool, is the account initialized. e.g. True or False.
    :return: Account immutable object.
    """
    return Account(
        is_active_card=is_active_card,
        available_limit=available_limit,
        is_initialized=is_initialized,
        is_premium=is_premium,
    )
