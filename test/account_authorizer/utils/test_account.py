# Python
import unittest

# Exceptions
from dataclasses import FrozenInstanceError

# Utils
from src.utils.account import Account


class TestAccountUtils(unittest.TestCase):

    def test_account_immutability(self):
        account = Account(is_active_card=True, available_limit=0, is_initialized=True, is_premium=False)
        with self.assertRaises(FrozenInstanceError):
            account.is_active_card = True


if __name__ == '__main__':
    unittest.main()
