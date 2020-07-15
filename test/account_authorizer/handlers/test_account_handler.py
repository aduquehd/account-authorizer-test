import unittest

from src.handlers.account_handler import initialize_account, new_account

from src.utils.account import Account


class TestAccountHandler(unittest.TestCase):

    def test_initialize_account(self):
        account = initialize_account()
        self.assertTrue(isinstance(account, Account))

        self.assertEqual(account.available_limit, 0)
        self.assertEqual(account.is_active_card, False)
        self.assertEqual(account.is_initialized, False)

    def test_create_new_account(self):
        account = new_account(is_active_card=True, available_limit=99)
        self.assertEqual(account.is_active_card, True)
        self.assertEqual(account.available_limit, 99)

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
