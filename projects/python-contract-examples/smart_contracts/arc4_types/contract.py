# pyright: reportMissingModuleSource=false
import typing as t

from algopy import ARC4Contract, GlobalState, UInt64, arc4, urange
from algopy.arc4 import abimethod


class Arc4Types(ARC4Contract):

    @abimethod()
    def arc4_uint64(self, a: arc4.UInt64, b: arc4.UInt64) -> arc4.UInt64:
        """
        This won't compile because you can't do math operations on arc4.UInt64 type.
        All arc4 types are backed by byte arrays on the AVM.
        c = a + b
        """

        # This is how you can do math operations on arc4.UInt64 type.
        c = a.native + b.native

        return arc4.UInt64(c)

    @abimethod()
    def arc4_address(self, address: arc4.Address) -> arc4.Address:
        underlying_bytes = (
            address.bytes
        )  # This will return the underlying bytes of the address.

        account = (
            address.native
        )  # This will return the account type of the given address.
        bal = account.balance
        num_asset_holding = account.total_assets

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
        todo = Todo(task=task, completed=arc4.Bool(False)) # noqa: FBT003

        if self.todos.value.length == 0:
            self.todos.value = Todos(todo.copy())
        else:
            self.todos.value.append(todo.copy())

        return self.todos.value

    @abimethod()
    def complete_todo(self, task: arc4.String) -> None:

        for index in urange(self.todos.value.length):
            if self.todos.value[index].task == task:
                self.todos.value[index].completed = arc4.Bool(True) # noqa: FBT003
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
