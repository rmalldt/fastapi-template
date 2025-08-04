def add(a: int, b: int):
    return a + b


def multiply(a: int, b: int):
    return a * b


class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self, starting_balance=0) -> None:
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in the account")
        self.balance -= amount

    def interest(self):
        self.balance *= 1.1
