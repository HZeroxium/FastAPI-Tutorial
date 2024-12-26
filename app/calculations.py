def add(num1: int, num2: int) -> int:
    return num1 + num2


def subtract(a: int, b: int) -> int:
    return a - b


def multiply(a: int, b: int) -> int:
    return a * b


class BankAccount:
    def __init__(self, balance: int = 0):
        self.balance = balance

    def deposit(self, amount: int):
        self.balance += amount
        return self.balance

    def withdraw(self, amount: int):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def collect_interest(self, rate: float = 0.1):
        self.balance += self.balance * rate
        return self.balance
