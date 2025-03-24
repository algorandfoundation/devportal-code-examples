from algopy import Account, ARC4Contract, BoxMap, Global, Txn, UInt64, gtxn
from algopy.arc4 import abimethod

COUNTER_BOX_KEY_LENGTH = 32 + 19
COUNTER_BOX_VALUE_LENGTH = 8
COUNTER_BOX_SIZE = COUNTER_BOX_KEY_LENGTH + COUNTER_BOX_VALUE_LENGTH
COUNTER_BOX_MBR = 2_500 + COUNTER_BOX_SIZE * 400


class BoxCounter(ARC4Contract):

    def __init__(self) -> None:
        self.account_box_counter = BoxMap(Account, UInt64)

    @abimethod
    def increment_box_counter(self, pay_mbr: gtxn.PaymentTransaction) -> UInt64:
        assert pay_mbr.amount == COUNTER_BOX_MBR
        assert pay_mbr.receiver == Global.current_application_address

        if Txn.sender in self.account_box_counter:
            self.account_box_counter[Txn.sender] += 1
        else:
            self.account_box_counter[Txn.sender] = UInt64(1)

        return self.account_box_counter[Txn.sender]
