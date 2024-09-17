from algopy import ARC4Contract, String
from algopy.arc4 import abimethod


class InnerTransactions(ARC4Contract):
    # example: payment
    @abimethod()
    def payment(self) -> UInt64:
        result = itxn.Payment(amount=5000, receiver=Txn.sender, fee=0).submit()
        return result.amount
    
    # fee is set to 0 by default. Manually set here for demonstration purposes.
    # The `Sender` for the above is implied to be Global.current_application_address().
    # If a different sender is needed, it'd have to be an account that has been rekeyed to the application address. 
    # example: payment
