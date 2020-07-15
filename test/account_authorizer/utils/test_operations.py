# Python
import unittest

# Utils
from src.utils.operations import get_event_type, get_operation_violations
from src.utils import violation_errors

# Handlers
from src.handlers.account_handler import new_account, initialize_account


class TestOperationsUtils(unittest.TestCase):

    def setUp(self):
        self.transaction_event1 = {
            "transaction": {"merchant": "TranX1", "amount": 10, "time": "2019-02-13T11:35:05.000Z"}}

        self.transaction_event2 = {
            "transaction": {"merchant": "TranX2", "amount": 20, "time": "2019-02-13T11:35:10.000Z"}}

        self.transaction_event3 = {
            "transaction": {"merchant": "TranX3", "amount": 30, "time": "2019-02-13T11:35:20.000Z"}}

        self.transaction_event4 = {
            "transaction": {"merchant": "TranX4", "amount": 40, "time": "2019-02-13T11:35:30.000Z"}}

        self.transaction_event5 = {
            "transaction": {"merchant": "TranX5", "amount": 50, "time": "2019-02-13T11:35:40.000Z"}}

        self.transaction_event6 = {
            "transaction": {"merchant": "TranX6", "amount": 60, "time": "2019-02-13T11:38:40.000Z"}}

        self.account_event = {"account": {"active-card": True, "available-limit": 1000}}
        self.operation = {"merchant": "Habbib's", "amount": 10, "time": "2019-02-13T11:36:00.000Z"}

    def test_get_event_type(self):
        event_type = get_event_type(self.transaction_event1)
        self.assertEqual(event_type, "transaction")

    def test_operation_violations(self):
        account = new_account(is_active_card=True, available_limit=100)
        previous_transactions = [
            self.transaction_event1, self.transaction_event2, self.transaction_event6
        ]
        violations = get_operation_violations(account, self.operation, previous_transactions)
        self.assertEqual(violations, [])

    def test_operation_violations_account_not_initialized(self):
        account = initialize_account()
        violations = get_operation_violations(account, self.operation, [])
        self.assertEqual(violations, [violation_errors.ACCOUNT_NOT_INITIALIZED])

    def test_operation_violations_insufficient_limits(self):
        account = new_account(is_active_card=True, available_limit=0)
        violations = get_operation_violations(account, self.operation, [])
        self.assertEqual(violations, [violation_errors.INSUFFICIENT_LIMITS])

    def test_operation_violations_card_not_active(self):
        account = new_account(is_active_card=False, available_limit=100)
        violations = get_operation_violations(account, self.operation, [])
        self.assertEqual(violations, [violation_errors.CARD_NOT_ACTIVE])

    def test_operation_violations_high_frequency_small_interval(self):
        account = new_account(is_active_card=True, available_limit=100)
        previous_transactions = [
            self.transaction_event1, self.transaction_event2, self.transaction_event3
        ]
        violations = get_operation_violations(account, self.operation, previous_transactions)
        self.assertEqual(violations, [violation_errors.HIGH_FREQUENCY_SMALL_INTERVAL])

    def test_operation_violations_double_transaction(self):
        account = new_account(is_active_card=True, available_limit=100)
        previous_transactions = [
            self.transaction_event1
        ]
        violations = get_operation_violations(account, self.transaction_event1['transaction'], previous_transactions)
        self.assertEqual(violations, [violation_errors.DOUBLED_TRANSACTION])


if __name__ == '__main__':
    unittest.main()
