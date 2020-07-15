# Python
import unittest

# Handlers
from src.handlers.operations_handler import (
    get_handler_by_transaction_type,
    _process_transaction_default,
    _process_transaction_event,
    _process_account_event
)
from src.handlers.account_handler import new_account, initialize_account

# Utils
from src.utils import violation_errors


class TestOperationsHandler(unittest.TestCase):
    def setUp(self):
        self.transaction_event = {
            "transaction": {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:35:00.000Z"}}
        self.transaction_event_2 = {
            "transaction": {"merchant": "Habbib's 2", "amount": 20, "time": "2019-02-13T11:35:10.000Z"}}
        self.transaction_event_3 = {
            "transaction": {"merchant": "Habbib's 3", "amount": 30, "time": "2019-02-13T11:35:30.000Z"}}
        self.transaction_event_4 = {
            "transaction": {"merchant": "Habbib's 4", "amount": 40, "time": "2019-02-13T11:35:40.000Z"}}
        self.account_event = {"account": {"active-card": True, "available-limit": 1000}}

    def test_handler_by_transaction_type(self):
        transaction_handler = get_handler_by_transaction_type("transaction")
        self.assertTrue(transaction_handler is _process_transaction_event)

        transaction_handler = get_handler_by_transaction_type("account")
        self.assertTrue(transaction_handler is _process_account_event)

        transaction_handler = get_handler_by_transaction_type("something-wrong")
        self.assertTrue(transaction_handler is _process_transaction_default)

    def test_process_account_event_with_initialized_account(self):
        account = new_account(is_active_card=True, available_limit=10)
        account, violations = _process_account_event(self.account_event, account, None)
        self.assertEqual(violations, [violation_errors.ACCOUNT_ALREADY_INITIALIZED])

    def test_process_account_event_with_not_initialized_account(self):
        account = initialize_account()
        account, violations = _process_account_event(self.account_event, account, None)
        self.assertEqual(violations, [])

    def test_process_transaction_default(self):
        one, two = _process_transaction_default(1, 2)
        self.assertEqual((one, two), (None, None))

    def test_process_transaction_event_with_insufficient_limits(self):
        account, violations = _process_transaction_event(
            event=self.transaction_event,
            account=new_account(is_active_card=True, available_limit=0),
            previous_transactions=[]
        )
        self.assertEqual(violations, [violation_errors.INSUFFICIENT_LIMITS])

    def test_process_transaction_event(self):
        account, violations = _process_transaction_event(
            event=self.transaction_event,
            account=new_account(is_active_card=True, available_limit=10),
            previous_transactions=[]
        )
        self.assertEqual(violations, [])

    def test_process_transaction_event_with_duplicated_transaction(self):
        account, violations = _process_transaction_event(
            event=self.transaction_event,
            account=new_account(is_active_card=True, available_limit=100),
            previous_transactions=[self.transaction_event]
        )
        self.assertEqual(violations, [violation_errors.DOUBLED_TRANSACTION])

    def test_process_transaction_event_with_high_frequency_transaction(self):
        account, violations = _process_transaction_event(
            event=self.transaction_event_4,
            account=new_account(is_active_card=True, available_limit=100),
            previous_transactions=[self.transaction_event, self.transaction_event_2, self.transaction_event_3]
        )
        self.assertEqual(violations, [violation_errors.HIGH_FREQUENCY_SMALL_INTERVAL])

    def test_process_transaction_event_with_premium_account(self):
        account, violations = _process_transaction_event(
            event=self.transaction_event,
            account=new_account(is_active_card=True, available_limit=100, is_premium=True),
            previous_transactions=[self.transaction_event],
        )
        self.assertEqual(violations, [])

        account, violations = _process_transaction_event(
            event=self.transaction_event_4,
            account=new_account(is_active_card=True, available_limit=100, is_premium=True),
            previous_transactions=[self.transaction_event, self.transaction_event_2, self.transaction_event_3]
        )
        self.assertEqual(violations, [])


if __name__ == '__main__':
    unittest.main()
