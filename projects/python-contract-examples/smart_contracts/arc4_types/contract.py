# pyright: reportMissingModuleSource=false
import typing as t

from algopy import ARC4Contract, GlobalState, UInt64, arc4, urange
from algopy.arc4 import abimethod


class Arc4Types(ARC4Contract):

    @abimethod()
    def arc4_uint64(self, a: arc4.UInt64, b: arc4.UInt64) -> arc4.UInt64:
        """
        Math operations (like a + b) are not supported on arc4.UInt64 types
        since they are internally represented as byte arrays in the AVM.
        Use the .native property to perform arithmetic operations.
        """

        # Use the native integers to perform arithmetic
        c = a.native + b.native

        return arc4.UInt64(c)

    @abimethod()
    def arc4_uint_n(
        self, a: arc4.UInt8, b: arc4.UInt16, c: arc4.UInt32, d: arc4.UInt64
    ) -> arc4.UInt64:
        """
        The encoding of arc4 integers will be smaller if it uses fewer bits.
        Ultimately, they are all represented with native UInt64.
        """
        assert a.bytes.length == 1
        assert b.bytes.length == 2
        assert c.bytes.length == 4
        assert d.bytes.length == 8

        total = a.native + b.native + c.native + d.native

        return arc4.UInt64(total)

    @abimethod()
    def arc4_biguint_n(self, a: arc4.UInt128, b: arc4.UInt256, c: arc4.UInt512) -> arc4.UInt512:
        """
        Integers with larger bit size are supported up to 512 bits.
        Ultimately, they are all represented with native BigUInt.
        """
        assert a.bytes.length == 16
        assert b.bytes.length == 32
        assert c.bytes.length == 64

        total = a.native + b.native + c.native

        return arc4.UInt512(total)

    @abimethod()
    def arc4_address_properties(self, address: arc4.Address) -> UInt64:
        underlying_bytes = (
            address.bytes
        )  # This will return the underlying bytes of the address.

        account = (
            address.native
        )  # This will return the account type of the given address.

        bal = account.balance  # returns the balance of the account
        total_asset = (
            account.total_assets
        )  # returns the total assets held in the account

        return bal

    @abimethod()
    def arc4_address_return(self, address: arc4.Address) -> arc4.Address:

        account = (
            address.native
        )  # This will return the account type of the given address.

        """
        You can't return an Account type because it is a reference type.
        Convert the Account type to arc4.Address type and return it.
        """
        converted_address = arc4.Address(account)

        assert converted_address == address

        return converted_address


AliasedStaticArray: t.TypeAlias = arc4.StaticArray[arc4.UInt8, t.Literal[1]]


class Arc4StaticArray(ARC4Contract):

    @abimethod()
    def arc4_static_array(self) -> None:
        """
        You can create a static array directly from the contract.
        """
        static_uint32_array = arc4.StaticArray(
            arc4.UInt32(1), arc4.UInt32(10), arc4.UInt32(255), arc4.UInt32(128)
        )

        total = UInt64(0)
        for uint32_item in static_uint32_array:
            total += uint32_item.native

        assert total == 1 + 10 + 255 + 128

        """
        You can also create a static array using a type alias.
        """
        aliased_static = AliasedStaticArray(arc4.UInt8(101))

        index = UInt64(0)

        assert (aliased_static[0].native + aliased_static[index].native) == 202

        """
        You can't modify the elements of a static array.
        so this won't compile:
        aliased_static[0] = arc4.UInt8(100)
        aliased_static.pop()
        """


class Todo(arc4.Struct):
    task: arc4.String
    completed: arc4.Bool


Todos: t.TypeAlias = arc4.DynamicArray[Todo]


class Arc4Struct(ARC4Contract):

    def __init__(self) -> None:
        self.todos = GlobalState(Todos())

    @abimethod()
    def add_todo(self, task: arc4.String) -> Todos:
        todo = Todo(task=task, completed=arc4.Bool(False))  # noqa: FBT003

        if self.todos.value.length == 0:
            self.todos.value = Todos(todo.copy())
        else:
            self.todos.value.append(todo.copy())

        return self.todos.value

    @abimethod()
    def complete_todo(self, task: arc4.String) -> None:

        for index in urange(self.todos.value.length):
            if self.todos.value[index].task == task:
                self.todos.value[index].completed = arc4.Bool(True)  # noqa: FBT003
                break

    @abimethod()
    def return_todo(self, task: arc4.String) -> Todo:
        todo_to_return: Todo

        exist = False
        for index in urange(self.todos.value.length):

            if self.todos.value[index].task == task:
                todo_to_return = self.todos.value[index].copy()
                exist = True

        assert exist

        return todo_to_return
