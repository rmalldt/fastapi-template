import math
from operator import mul
import pytest
import pytest
from app.sample import add, multiply, BankAccount, InsufficientFunds


@pytest.fixture
def account_default():
    print("Creating default account")
    return BankAccount()


@pytest.fixture
def account_initial_value():
    print("Creating account with initial value")
    return BankAccount(50)


def test_add():
    print("Testing add function")
    sum = add(2, 3)
    assert sum == 5


@pytest.mark.parametrize("a, b, expected", [(2, 2, 4), (2, 3, 6), (3, 3, 9)])
def test_multiply(a, b, expected):
    print("Testing multiply")
    assert multiply(a, b) == expected


def test_bank_default_amount(account_default):
    print("Testing BankAccount default amount")
    assert account_default.balance == 0


def test_bank_set_initial_amount(account_initial_value):
    print("Testing BankAccount initial amount")
    assert account_initial_value.balance == 50


def test_bank_deposit(account_initial_value):
    print("Testing BankAccount deposit")
    account_initial_value.deposit(30)
    assert account_initial_value.balance == 80


def test_bank_withdraw(account_initial_value):
    print("Testing BankAccount withdraw")
    account_initial_value.withdraw(30)
    assert account_initial_value.balance == 20


def test_bank_interest(account_initial_value):
    print("Testing BankAccount interest")
    account_initial_value.interest()
    assert round(account_initial_value.balance, 2) == 55


@pytest.mark.parametrize(
    "deposited, withdrew, expected",
    [(200, 100, 100), (50, 30, 20), (1200, 200, 1000)],
)
def test_bank_transaction(account_default, deposited, withdrew, expected):
    print("Testing BankAccount transaction")
    account_default.deposit(deposited)
    account_default.withdraw(withdrew)
    assert account_default.balance == expected


def test_withdraw_insufficient_fund(account_initial_value):
    with pytest.raises(InsufficientFunds):
        account_initial_value.withdraw(200)
