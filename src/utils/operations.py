# Python utils
import datetime

# Utils
from src.utils import violation_errors

# Handlers
from src.handlers.account_handler import new_account


def get_event_type(event):
    """
    Get the operations type or None, if there'is an exception or has an invalid type.
    :param event: Dict, a single event data. e.g.
        {"transaction": {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}}
    :return: String, operation type. e.g. "transaction" or "account" or None if is an invalid type.
    """
    try:
        operation_type = list(event.keys())[0]
        if operation_type not in ["transaction", "account"]:
            return None
        return operation_type
    except Exception:
        return None


def get_operation_violations(account, operation, previous_transactions):
    """
    Get the violations by an operation.
    :param account: Account Immutable object.
    :param operation: Dict, Current transaction operation. e.g.
        {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}
    :param previous_transactions: List, previous transaction list. e.g.
        {"transaction": {"merchant": "Burger King", "amount": 50, "time": "2019-02-13T10:55:50.000Z"}}
        {"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:35:00.000Z"}}
    :return: List, violations to apply. e.g.
        ['insufficient-limit', 'high-frequency-small-interval']
    """
    violations = []

    violations.extend(_base_account_operation_violations(account, operation))
    violations.extend(_basic_account_operation_violations(account, operation, previous_transactions))

    return violations


def _base_account_operation_violations(account, operation):
    violations = []
    if not account.is_initialized:
        violations.append(violation_errors.ACCOUNT_NOT_INITIALIZED)
        return violations

    if operation['amount'] > account.available_limit:
        violations.append(violation_errors.INSUFFICIENT_LIMITS)

    if not account.is_active_card:
        violations.append(violation_errors.CARD_NOT_ACTIVE)

    return violations


def _basic_account_operation_violations(account, operation, previous_transactions):
    violations = []
    if not account.is_premium:
        high_frequency_violations = _get_operation_high_frequency_violations(operation, previous_transactions)
        if high_frequency_violations:
            violations.append(high_frequency_violations)

        doubled_transaction_violations = _get_operation_doubled_transaction_violations(operation, previous_transactions)
        if doubled_transaction_violations:
            violations.append(doubled_transaction_violations)
    return violations


def _get_operation_high_frequency_violations(operation, previous_transactions):
    """
    Check if exist more than 3 transaction on a 2-minutes interval.
    :param operation: Dict, Current transaction operation. e.g.
        {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}
    :param previous_transactions: List, previous transaction list. e.g.
        {"transaction": {"merchant": "Burger King", "amount": 50, "time": "2019-02-13T10:55:50.000Z"}}
        {"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:35:00.000Z"}}
    :return: String, the violation "high-frequency-small-interval" or None.
    """
    operation_time = datetime.datetime.strptime(operation['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    min_date_range = operation_time - datetime.timedelta(minutes=2)
    transaction_in_last_2_minutes_count = 0

    for transaction in previous_transactions:
        transaction_date = datetime.datetime.strptime(transaction['transaction']['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if min_date_range <= transaction_date <= operation_time:
            transaction_in_last_2_minutes_count += 1

    if transaction_in_last_2_minutes_count > 2:
        return violation_errors.HIGH_FREQUENCY_SMALL_INTERVAL


def _get_operation_doubled_transaction_violations(operation, previous_transactions):
    """
    Check if exist more than 3 transaction on a 2-minutes interval.
    :param operation: Dict, Current transaction operation. e.g.
        {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}
    :param previous_transactions: List, previous transaction list. e.g.
        {"transaction": {"merchant": "Burger King", "amount": 50, "time": "2019-02-13T10:55:50.000Z"}}
        {"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:35:00.000Z"}}
    :return: String, the violation "high-frequency-small-interval" or None.
    """
    operation_time = datetime.datetime.strptime(operation['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    min_date_range = operation_time - datetime.timedelta(minutes=2)

    for transaction in previous_transactions:
        transaction_date = datetime.datetime.strptime(transaction['transaction']['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if transaction['transaction']['merchant'] == operation['merchant']:
            if transaction['transaction']['amount'] == operation['amount']:
                if min_date_range <= transaction_date <= operation_time:
                    return violation_errors.DOUBLED_TRANSACTION


def execute_operation_amount_transaction(account, amount):
    """
    Update the account available limit if the account is initialized, has an active card and the amount is less or
    equal than the current available limit.
    The account object is immutable, so this method create a new account object with the new values.
    :param account: Account immutable object.
    :param amount: Float, amount value to decrease into the limit.
    :return: Account immutable object.
    """
    if account.is_initialized and account.is_active_card and amount <= account.available_limit:
        new_available_limit = account.available_limit - amount
        account = new_account(
            is_active_card=True,
            available_limit=new_available_limit,
            is_premium=account.is_premium,
        )
    return account
