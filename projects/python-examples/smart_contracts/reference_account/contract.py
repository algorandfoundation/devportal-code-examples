# example: ACCOUNT_REFERENCE_EXAMPLE
from algopy import Account, ARC4Contract, UInt64
from algopy.arc4 import abimethod

"""
A contract that demonstrates how to use resource usage in a contract using an account reference
"""


class ReferenceAccount(ARC4Contract):
    """
    Returns the balance of the account
    @returns The balance of the account
    """

    @abimethod
    def get_account_balance(self) -> UInt64:
        return Account(
            "WMHF4FLJNKY2BPFK7YPV5ID6OZ7LVDB2B66ZTXEAMLL2NX4WJZRJFVX66M"
        ).balance  # Replace with your account address

    """
    Returns the balance of the account
    @param account The account to get the balance of
    @returns The balance of the account
    """

    @abimethod
    def get_account_balance_with_argument(self, account: Account) -> UInt64:
        return account.balance


# example: ACCOUNT_REFERENCE_EXAMPLE
