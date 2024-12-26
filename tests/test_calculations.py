# from app.calculations import add, subtract, BankAccount
# import pytest


# @pytest.fixture
# def zero_bank_account():
#     return BankAccount()


# @pytest.fixture
# def hundred_bank_account():
#     return BankAccount(100)


# # @pytest.mark.parametrize(
# #     "num1, num2, expected", [(1, 2, 3), (0, 0, 0), (-1, 1, 0), (-1, -1, -2)]
# # )
# # def test_add(num1: int, num2: int, expected: int):
# #     assert add(num1, num2) == expected


# # def test_bank_set_initial_balance():
# #     account = BankAccount(100)
# #     assert account.balance == 100


# # def test_bank_default_initial_balance(zero_bank_account):
# #     assert zero_bank_account.balance == 0


# # def test_withdraw():
# #     account = BankAccount(100)
# #     assert account.withdraw(50) == 50


# # def test_deposit():
# #     account = BankAccount(100)
# #     assert account.deposit(50) == 150


# # def test_collect_interest():
# #     account = BankAccount(100)
# #     assert account.collect_interest(rate=0.1) == 110


# @pytest.mark.parametrize("deposit, withdraw, expected", [(100, 50, 50), (100, 100, 0)])
# def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
#     zero_bank_account.deposit(deposit)
#     zero_bank_account.withdraw(withdraw)
#     assert zero_bank_account.balance == expected


# def test_insufficient_funds(zero_bank_account):
#     with pytest.raises(ValueError):
#         zero_bank_account.withdraw(50)
