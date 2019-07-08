import unittest

from functions import Matomat
from functions.Matomat import INVALID_DEPOSIT_ARGS, MAXIMUM_DEPOSIT, MINIMUM_DEPOSIT, TOO_MANY_DEPOSITS
from neocortex.memories import TRANSACTION_FLOODING_THRESHOLD, DEPOSIT_FLOODING_THRESHOLD
from tests.test import mock_telegram_user


class TestMatomat(unittest.TestCase):

    def test_add_product_wrong_format(self):
        answer = Matomat.add_product([])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["", ""])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["a", ""])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["b", "(0.3€"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["c", "0.3€"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["d", "0.3€)"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["e", "0.3"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["f", "(.€)"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["g", "(.)"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["h", "()"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["i", "(3)"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["j", "(99.99991€)"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["k", "(100€)"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

        answer = Matomat.add_product(["l", "(l)"])
        self.assertEqual(Matomat.INVALID_ADD_ARGS, answer)

    def test_add_product(self):
        answer = Matomat.add_product(["matomat", "(0.7€)"])
        self.assertEqual(f"matomat (0.70€) added.", answer)

        answer = Matomat.add_product(["a", "(3€)"])
        self.assertEqual(f"a (3.00€) added.", answer)

        answer = Matomat.add_product(["b", "(2,2€)"])
        self.assertEqual(f"b (2.20€) added.", answer)

        answer = Matomat.add_product(["c", "(2.25€)"])
        self.assertEqual(f"c (2.25€) added.", answer)

        answer = Matomat.add_product(["e", "(9.994€)"])
        self.assertEqual(f"e (9.99€) added.", answer)

        answer = Matomat.add_product(["f", "(9.996€)"])
        self.assertEqual(f"f (10.00€) added.", answer)

        answer = Matomat.add_product(["g", "(99,99€)"])
        self.assertEqual(f"g (99.99€) added.", answer)

    def test_deposit(self):
        user_a = mock_telegram_user("User A")
        answer = Matomat.deposit(user_a, [""])
        self.assertEqual(INVALID_DEPOSIT_ARGS, answer)

        answer = Matomat.deposit(user_a, ["30€"])
        self.assertEqual("Your new balance is 30.00€", answer)

        answer = Matomat.deposit(user_a, ["1"])
        self.assertEqual("Your new balance is 31.00€", answer)

        answer = Matomat.deposit(user_a, ["-2€"])
        self.assertEqual("Your new balance is 33.00€", answer)

        answer = Matomat.deposit(user_a, ["0.1€"])
        self.assertEqual("Your new balance is 33.10€", answer)

        answer = Matomat.deposit(user_a, [f"{MAXIMUM_DEPOSIT + 0.01}€"])
        self.assertEqual(f"Deposits above {MAXIMUM_DEPOSIT:.2f}€ are not allowed.", answer)

        answer = Matomat.deposit(user_a, ["""񣲪竖|QRښ׎翬γGӰߣ궰񸏭셋;ӓ񲯯迖ެ)Ⱦڲە◈䤦IhԻח
                                             𙅱򞗫ʮ鏑񇑋뱟б󥼛󖠲^5@󩎖襺ѓXꂟ򊗎ӽ򣮰Ԇ;w񜽺⢝룕􊂑ֻ쑅s
                                             󨈴`Új򎢅Ұǌ(hㅌݼӀᚔ􂋄嵝񲖙􌛲ʣꁜ{򺼰Ģߓ򯺾񔮵򎷮𿜪唥f𾴗ǐ
                                             C􃌨񾹻Stشgꄬ𴢿�򙏁𣮞㝁,ŗP癇蠪穀󭀼择\㙿Ƶ՟򄕸Ә񆞏񄞓N翋
                                          ٳڗ󉫉̑Է򒰜𦆢6򙩑򐕭󅩲𪭳O󐁝{Ǔѿѡ󧮄񲫘7꿋'㲔o򥂉篗إHa"""])
        self.assertEqual(INVALID_DEPOSIT_ARGS, answer)

        user_b = mock_telegram_user("User B")  # we create a new user here to prevent a ban of A by flooding protection

        answer = Matomat.deposit(user_b, ["0.01€"])
        self.assertEqual("Your new balance is 0.01€", answer)

        answer = Matomat.deposit(user_b, ["50.00€"])
        self.assertEqual(f"You are trying to deposit over {MAXIMUM_DEPOSIT:.2f}€. "
                         f"We only sell Mate in 'haushaltsüblichen Mengen'. Please don't leave so much cash here.",
                         answer)

        answer = Matomat.deposit(user_b, ["0.00€"])
        self.assertEqual(f"Deposits below {MINIMUM_DEPOSIT}€ are not allowed.", answer)
        pass

    def test_deposit_flooding_protection(self):
        user = mock_telegram_user("spamming_boi")
        for i in range(DEPOSIT_FLOODING_THRESHOLD + 1):
            Matomat.deposit(user, ["0.01"])
        answer = Matomat.deposit(user, ["0.01"])
        self.assertEqual(TOO_MANY_DEPOSITS, answer)
        pass
