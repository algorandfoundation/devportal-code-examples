# example: REFERENCE_APP_BOX_EXAMPLE

from algopy import Account, ARC4Contract, BoxMap, Global, GlobalState, Txn, UInt64, gtxn
from algopy.arc4 import abimethod

"""
A contract that uses box storage to maintain a counter for each account
Each account needs to pay for the Minimum Balance Requirement (MBR) for their box
Constants for box storage are stored in global state
"""

COUNTER_BOX_KEY_LENGTH = 32 + 19
COUNTER_BOX_VALUE_LENGTH = 8


class ReferenceAppBox(ARC4Contract):
    def __init__(self) -> None:
        # Define constants for box storage in global state
        self.key_length = GlobalState(
            UInt64(COUNTER_BOX_KEY_LENGTH)
        )  # Account address (32 bytes) + key prefix overhead (19 bytes)
        self.value_length = GlobalState(
            UInt64(COUNTER_BOX_VALUE_LENGTH)
        )  # uint64 (8 bytes)
        self.box_size = GlobalState(UInt64)  # Calculated in constructor
        self.box_mbr = GlobalState(UInt64)  # Calculated in constructor

        # Create a box map to store counter values per account
        self.account_box_counter = BoxMap(Account, UInt64, key_prefix="counter")

    @abimethod(create="require")
    def create(self) -> None:
        self.box_size.value = self.key_length.value + self.value_length.value
        self.box_mbr.value = UInt64(2_500) + self.box_size.value * UInt64(
            400
        )  # Base MBR + (size * per-byte cost)

    """
    Increments the counter for the transaction sender
    Requires a payment transaction to cover the MBR for the box
    @param payMbr Payment transaction covering the box MBR
    @returns The new counter value
    """

    @abimethod
    def increment_box_counter(self, pay_mbr: gtxn.PaymentTransaction) -> UInt64:
        # Verify the payment covers the MBR cost and is sent to the contract
        assert pay_mbr.amount == self.box_mbr.value, "Payment must cover the box MBR"
        assert (
            pay_mbr.receiver == Global.current_application_address
        ), "Payment must be to the contract"

        counter, has_counter = self.account_box_counter.maybe(Txn.sender)

        if has_counter:
            self.account_box_counter[Txn.sender] += 1
            return self.account_box_counter[Txn.sender]
        else:
            self.account_box_counter[Txn.sender] = UInt64(1)
            return UInt64(1)

    """
    Gets the current counter value for the transaction sender
    @returns The current counter value or 0 if not set
    """

    @abimethod(readonly=True)
    def get_box_counter(self) -> UInt64:
        counter, has_counter = self.account_box_counter.maybe(Txn.sender)
        if has_counter:
            return counter
        return UInt64(0)

    """
    Gets the current counter value for any account
    @param account The account to check
    @returns The current counter value or 0 if not set
    """

    @abimethod(readonly=True)
    def get_box_counter_for_account(self, account: Account) -> UInt64:
        counter, has_counter = self.account_box_counter.maybe(account)
        if has_counter:
            return counter
        return UInt64(0)

    """
    Returns the MBR cost for creating a box
    @returns The MBR cost in microAlgos
    """

    @abimethod(readonly=True)
    def get_box_mbr(self) -> UInt64:
        return self.box_mbr.value

    """
    Returns all the box size configuration values
    @returns A tuple containing [keyLength, valueLength, boxSize, boxMbr]
    """

    @abimethod(readonly=True)
    def get_box_configuration(self) -> tuple[UInt64, UInt64, UInt64, UInt64]:
        return (
            self.key_length.value,
            self.value_length.value,
            self.box_size.value,
            self.box_mbr.value,
        )

    """
    Updates the box size configuration values
    @param newKeyLength The new key length
    @param newValueLength The new value length
    """

    @abimethod
    def update_box_configuration(
        self, new_key_length: UInt64, new_value_length: UInt64
    ) -> None:
        self.key_length.value = new_key_length
        self.value_length.value = new_value_length

        # Recalculate derived values
        self.box_size.value = self.key_length.value + self.value_length.value
        self.box_mbr.value = UInt64(2_500) + self.box_size.value * UInt64(400)


# example: REFERENCE_APP_BOX_EXAMPLE
