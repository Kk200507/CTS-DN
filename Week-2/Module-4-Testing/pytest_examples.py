"""
Module 4: Testing - PyTest Examples
---------------------------------------------------------------------
This file demonstrates writing test suites using PyTest, covering 
fixtures, parametrization, testing exceptions, and markers.
---------------------------------------------------------------------
"""

import pytest

# =====================================================================
# Target Code to Test
# =====================================================================
class InsufficientFundsError(Exception):
    pass


class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = initial_balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Balance is {self.balance}.")
        self.balance -= amount


# =====================================================================
# PyTest Fixtures
# =====================================================================
# Fixtures provide a fixed baseline upon which tests can reliably run.

@pytest.fixture(scope="function")
def empty_account():
    """Returns a fresh empty BankAccount for every test function."""
    return BankAccount("Alice")


@pytest.fixture(scope="function")
def funded_account():
    """Returns a funded BankAccount for every test function."""
    return BankAccount("Bob", 100.0)


# =====================================================================
# Basic Assertions & Fixture Usage
# =====================================================================

def test_initial_balance(empty_account):
    # Tests that the fixture setup the correct default balance
    assert empty_account.balance == 0.0
    assert empty_account.owner == "Alice"


def test_deposit(funded_account):
    # Act
    funded_account.deposit(50.0)
    # Assert
    assert funded_account.balance == 150.0


# =====================================================================
# Exception Testing
# =====================================================================
# Use `pytest.raises` to assert that a block of code raises a specific exception.

def test_deposit_negative_amount_raises_value_error(empty_account):
    with pytest.raises(ValueError) as exc_info:
        empty_account.deposit(-10.0)
    
    # Assert exact error message match
    assert str(exc_info.value) == "Deposit amount must be positive."


def test_withdraw_overdraft_raises_insufficient_funds(funded_account):
    with pytest.raises(InsufficientFundsError):
        funded_account.withdraw(150.0)


# =====================================================================
# Parametrized Tests
# =====================================================================
# Parametrization allows running the same test multiple times with 
# different inputs and expected outputs, reducing duplicate test code.

@pytest.mark.parametrize(
    "deposit_amt, withdraw_amt, expected_balance",
    [
        (50.0, 20.0, 130.0),  # Regular transactions
        (100.0, 100.0, 100.0),# Withdraw matches deposit
        (0.01, 0.01, 100.0),  # Tiny amounts
    ]
)
def test_account_transaction_combinations(funded_account, deposit_amt, withdraw_amt, expected_balance):
    funded_account.deposit(deposit_amt)
    funded_account.withdraw(withdraw_amt)
    assert funded_account.balance == expected_balance


# =====================================================================
# Custom Markers
# =====================================================================
# Markers categorize tests. Run specific markers using: pytest -m slow

@pytest.mark.slow
def test_slow_simulation(empty_account):
    # A dummy test marked as 'slow'
    import time
    # In actual usage this would simulate slower integration operations
    time.sleep(0.1) 
    assert True
