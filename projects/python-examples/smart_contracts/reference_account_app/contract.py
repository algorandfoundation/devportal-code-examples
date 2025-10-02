# example: REFERENCE_ACCOUNT_APP_EXAMPLE
from algopy import (
    Account,
    Application,
    ARC4Contract,
    Global,
    LocalState,
    Txn,
    UInt64,
    op,
)
from algopy.arc4 import abimethod

"""
A contract that maintains a per-account counter in local state
Accounts must opt in to use the counter
"""


class MyCounter(ARC4Contract):
    def __init__(self) -> None:
        # Define a local state variable for the counter
        self.my_counter = LocalState(UInt64)

    """
    Initialize the counter when an account opts in
    """

    @abimethod(allow_actions=["OptIn"])
    def opt_in(self) -> None:
        self.my_counter[Txn.sender] = UInt64(0)

    """
    Increment the counter for the sender and return its new value
    @returns The new counter value
    """

    @abimethod
    def increment_my_counter(self) -> UInt64:
        assert Txn.sender.is_opted_in(Global.current_application_id)

        self.my_counter[Txn.sender] += 1
        return self.my_counter[Txn.sender]


"""
A contract that demonstrates how to reference accounts and applications
to access local state from external contracts
"""


class ReferenceAccountApp(ARC4Contract):
    """
    Get the counter value from another account's local state with hardcoded values
    @returns The counter value or 0 if it doesn't exist
    """

    @abimethod
    def get_my_counter(self) -> UInt64:
        acct = Account(
            "WMHF4FLJNKY2BPFK7YPV5ID6OZ7LVDB2B66ZTXEAMLL2NX4WJZRJFVX66M"
        )  # Replace with your account address
        app = Application(1717)  # Replace with your application id

        # Check if the counter value exists in the account's local state for the specified app
        my_count, exist = op.AppLocal.get_ex_uint64(acct, app, b"my_counter")
        if not exist:
            return UInt64(0)
        return my_count

    """
    Get the counter value from another account's local state with provided parameters
    @param account The account to check
    @param app The application to query
    @returns The counter value or 0 if it doesn't exist
    """

    @abimethod
    def get_my_counter_with_arg(self, acct: Account, app: Application) -> UInt64:
        # Check if the counter value exists in the account's local state for the specified app
        my_count, exist = op.AppLocal.get_ex_uint64(acct, app, b"my_counter")
        if not exist:
            return UInt64(0)
        return my_count


# example: REFERENCE_ACCOUNT_APP_EXAMPLE
