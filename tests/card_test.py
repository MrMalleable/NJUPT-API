import unittest

from njupt.exceptions import AuthenticationException, UnauthorizedError, NjuptException
from njupt.models.card import Card
from tests.account_for_test import card_account, card_right_password, card_wrong_password


class CardTestCase(unittest.TestCase):
    """
    test card， need define account right password and wrong password before test
    """

    def test_not_login(self):
        card = Card()
        self.assertRaises(UnauthorizedError, card.get_balance)

    def test_login(self):
        card = Card()
        self.assertEqual(0, card.login(card_account, card_right_password)['code'])
        self.assertTrue(card.login(card_account, card_right_password)['success'])
        self.assertRaises(AuthenticationException, card.login, card_account, card_wrong_password)

    def test_balance(self):
        card = Card()
        card.login(card_account, card_right_password)
        self.assertGreaterEqual(card.get_balance()['total'], 0)

    def test_bill(self):
        card = Card(account=card_account, password=card_right_password)
        self.assertIn('recodes', card.get_bill())

    def test_net(self):
        card = Card(account=card_account, password=card_right_password)
        self.assertGreaterEqual(card.get_net_balance(), 0)

    def test_recharge(self):
        card = Card(account=card_account, password=card_right_password)
        self.assertTrue(card.recharge_xianlin_elec(0.01, '兰苑11栋', '4031')['success'])
        self.assertRaises(NjuptException, card.recharge_xianlin_elec, 0.01, '稀奇古怪栋', '4031')
        self.assertFalse(card.recharge_xianlin_elec(-0.01, '兰苑11栋', '4031')['success'])
