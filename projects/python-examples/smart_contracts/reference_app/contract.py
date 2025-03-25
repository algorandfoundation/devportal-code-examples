# example: APP_REFERENCE_EXAMPLE

from algopy import Application, ARC4Contract, UInt64, arc4
from algopy.arc4 import abimethod

"""
A contract that increments a counter
"""


class Counter(ARC4Contract):

    def __init__(self) -> None:
        self.counter = UInt64(0)

    """
    Increments the counter and returns the new value
    @returns The new counter value
    """

    @abimethod
    def increment(self) -> UInt64:
        self.counter += 1
        return self.counter


"""
A contract that demonstrates how to use resource usage in a contract using an asset reference
"""


class ReferenceApp(ARC4Contract):
    """
    Calls the increment method on another Counter app with a hardcoded app ID
    @returns The incremented counter value from the inner call
    """

    @abimethod
    def increment_via_inner(self) -> UInt64:
        app = Application(1717)  # Replace with your application id

        counter_result, call_txn = arc4.abi_call(
            Counter.increment,
            fee=0,
            app_id=app,
        )
        return counter_result

    """
    Calls the increment method on another Counter app passed as an argument
    @param app The application to call
    @returns The incremented counter value from the inner call
    """

    @abimethod
    def increment_via_inner_with_arg(self, app: Application) -> UInt64:
        # Call the increment method on the provided Counter application
        counter_result, call_txn = arc4.abi_call(Counter.increment, fee=0, app_id=app)
        return counter_result


# example: APP_REFERENCE_EXAMPLE
