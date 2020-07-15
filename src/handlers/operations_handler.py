# Utils
from src.utils.operations import get_event_type, get_operation_violations, execute_operation_amount_transaction
from src.utils import violation_errors

# Handlers
from src.handlers.account_handler import initialize_account, new_account


def process_events(event_list):
    """
    Process all event/operation.
        - Create validations/violations
        - Execute a transaction (Update account state)
    :param event_list:  List, operation list to validate and execute. e.g.
        {"account": {"active-card": true, "available-limit": 100}}
        {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}
    :return: TODO
    """
    account = initialize_account()
    operation_result_list = []
    previous_transactions = []

    for index, event in enumerate(event_list):
        try:
            account, operation_result = _process_event(previous_transactions, event, account)
            if operation_result:
                operation_result_list.append(operation_result)
                if 'transaction' in event:
                    previous_transactions.append(event)
        except Exception:
            continue
    return operation_result_list


def _process_event(previous_transactions, event, account):
    """
    Process all events.
    :param previous_transactions: List, previous transaction list. e.g.
        {"transaction": {"merchant": "Burger King", "amount": 50, "time": "2019-02-13T10:55:50.000Z"}}
        {"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:35:00.000Z"}}
    :param event: Dict, a single event data. e.g.
        {"transaction": {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}}
    :param account: Account immutable object.
    :return: Account Immutable object, List -> Operation result.
    """
    event_type = get_event_type(event)
    operation_handler = get_handler_by_transaction_type(event_type)
    account, violations = operation_handler(event, account, previous_transactions)

    if account:
        operation_result = {
            'account': {
                'active-card': account.is_active_card,
                'available-limit': account.available_limit,
            },
            'violations': violations
        }
        return account, operation_result
    else:
        return account, None


def _process_account_event(event, account, _):
    """
    Process account event.
    :param event: Dict, a single event data. e.g.
        {"transaction": {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}}
    :param account: Account immutable object.
    :param _: None.
    :return: Account immutable object, List of violations.
    """
    violations = []

    if account.is_initialized:
        violations.append(violation_errors.ACCOUNT_ALREADY_INITIALIZED)
    else:
        account = new_account(
            is_active_card=event['account']['active-card'],
            available_limit=event['account']['available-limit'],
            is_initialized=True,
            is_premium=event['account'].get('is-premium', False),
        )

    return account, violations


def _process_transaction_event(event, account, previous_transactions):
    """
    Process a single transaction event
    :param event: Dict, a single event data. e.g.
        {"transaction": {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}}
    :param account: Account immutable object.
    :param previous_transactions: List, previous transaction list. e.g.
        {"transaction": {"merchant": "Burger King", "amount": 50, "time": "2019-02-13T10:55:50.000Z"}}
        {"transaction": {"merchant": "Habbib's", "amount": 90, "time": "2019-02-13T11:35:00.000Z"}}
    :return: Account immutable object, List of violations.
    """
    operation = event['transaction']
    violations = get_operation_violations(account=account, operation=operation,
                                          previous_transactions=previous_transactions)
    if not violations:
        account = execute_operation_amount_transaction(account, operation['amount'])
    return account, violations


def _process_transaction_default(event, account):
    """Return a transaction default"""
    return None, None


def get_handler_by_transaction_type(transaction_type):
    """
    Get the correct handler by a transaction type "transaction" or "account".
    Return a default transaction with no behavior if the type doesn't exists.
    :param transaction_type: String, transaction type -> "transaction" or "account"
    :return: Object, function by reference to execute.
    """
    switcher = {
        'account': _process_account_event,
        'transaction': _process_transaction_event,
    }
    return switcher.get(transaction_type, _process_transaction_default)
