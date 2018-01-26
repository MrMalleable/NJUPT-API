import unittest
from pprint import pprint

from njupt.models.card import Card
from tests.account_for_test import card_account, card_right_password, card_wrong_password


class CardTestCase(unittest.TestCase):
    """
    test card， need define account right password and wrong password before test
    """

    def test_login(self):
        card = Card()
        self.assertEqual(0, card.login(card_account, card_right_password)['errorCode'])
        self.assertEqual(1, card.login(card_account, card_wrong_password)['errorCode'])

    def test_balance(self):
        card = Card()
        card.login(card_account, card_right_password)
        self.assertGreaterEqual(card.get_balance(), 0)

    def test_bill(self):
        card = Card(account=card_account, password=card_right_password)
        self.assertIn('recodes', card.get_bill())