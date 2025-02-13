# pyright: reportMissingModuleSource=false
import typing as t

from algopy import (
    ARC4Contract,
    GlobalState,
    String,
    UInt64,
    arc4,
    urange,
)
from algopy.arc4 import abimethod


class Arc4Types(ARC4Contract):

    # example: ARC4_UINT64
    @abimethod()
    def add_arc4_uint64(self, a: arc4.UInt64, b: arc4.UInt64) -> arc4.UInt64:
        """
        Math operations (like a + b) are not supported on arc4.UInt64 types
        since they are internally represented as byte arrays in the AVM.
        Use the .native property to perform arithmetic operations.
        """

        # Use the native integers to perform arithmetic
        c = a.native + b.native

        # Convert back to arc4.UInt64 for ABI compatability before returning
        return arc4.UInt64(c)

    # example: ARC4_UINT64

    # example: ARC4_UINTN
    @abimethod()
    def add_arc4_uint_n(
        self, a: arc4.UInt8, b: arc4.UInt16, c: arc4.UInt32, d: arc4.UInt64
    ) -> arc4.UInt64:
        """
        The encoding of arc4 integers will be smaller if it uses fewer bits.
        Ultimately, they are all represented with native UInt64.
        """
        assert a.bytes.length == 1  # UInt8 = 1 byte
        assert b.bytes.length == 2  # UInt16 = 2 bytes
        assert c.bytes.length == 4  # UInt32 = 4 bytes
        assert d.bytes.length == 8  # UInt64 = 8 bytes

        total = a.native + b.native + c.native + d.native

        return arc4.UInt64(total)

    # example: ARC4_UINTN

    # example: ARC4_BIGUINT
    @abimethod()
    def add_arc4_biguint_n(
        self, a: arc4.UInt128, b: arc4.UInt256, c: arc4.UInt512
    ) -> arc4.UInt512:
        """
        Integers with larger bit size are supported up to 512 bits.
        Ultimately, they are all represented with native BigUInt.
        """
        assert a.bytes.length == 16
        assert b.bytes.length == 32
        assert c.bytes.length == 64

        total = a.native + b.native + c.native

        return arc4.UInt512(total)

    # example: ARC4_BIGUINT

    # example: ARC4_BYTES
    @abimethod()
    def arc4_byte(self, a: arc4.Byte) -> arc4.Byte:
        """
        An arc4.Byte is essentially an alias for an 8-bit integer.
        """
        return arc4.Byte(a.native + 1)

    # example: ARC4_BYTES

    # example: ARC4_ADDRESS
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

    # example: ARC4_ADDRESS


# example: ARC4_STATIC_ARRAY
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

        aliased_static[0] = arc4.UInt8(202)

        assert aliased_static[0].native == 202

        """
        You can't add or pop values from a static array because it has a fixed size.
        so this won't compile:
        aliased_static.pop()
        """


# example: ARC4_STATIC_ARRAY

# example: ARC4_DYNAMIC_ARRAY
goodbye: t.TypeAlias = arc4.DynamicArray[arc4.String]


class Arc4DynamicArray(ARC4Contract):

    @abimethod
    def goodbye(self, name: arc4.String) -> goodbye:
        bye = goodbye(arc4.String("Good bye "), name)

        return bye

    @abimethod()
    def hello(self, name: arc4.String) -> String:
        """
        Dynamic Arrays have variable size and capacity.
        They are similar to native Python lists because they can also append, extend, and pop.
        """
        dynamic_string_array = arc4.DynamicArray[arc4.String](arc4.String("Hello "))

        extension = arc4.DynamicArray[arc4.String](name, arc4.String("!"))
        dynamic_string_array.extend(extension)

        copied_dynamic_string_array = dynamic_string_array.copy()
        copied_dynamic_string_array.pop()
        copied_dynamic_string_array.pop()
        copied_dynamic_string_array.append(arc4.String("world!"))

        greeting = String()
        for x in dynamic_string_array:
            greeting += x.native

        return greeting

    # example: ARC4_DYNAMIC_ARRAY

    # example: ARC4_DYNAMIC_BYTES
    @abimethod()
    def arc4_dynamic_bytes(self) -> arc4.DynamicBytes:
        """arc4.DynamicBytes is essentially an arc4.DynamicArray[arc4.Byte] with additional convenience methods"""
        dynamic_bytes = arc4.DynamicBytes(b"\xff\xff\xff")

        # arc4.DynamicBytes can return the native bytearray instead of accessing every single index of the array.
        # This is only true for arc4.DynamicBytes because, as an example, an arc4.DynamicArray[arc4.UInt64]
        #  doesn't have a native equivalent.
        native_dynamic_bytes = dynamic_bytes.native

        dynamic_bytes[0] = arc4.Byte(0)

        dynamic_bytes.extend(arc4.DynamicBytes(b"\xaa\xbb\xcc"))
        dynamic_bytes.pop()
        dynamic_bytes.append(arc4.Byte(255))

        return dynamic_bytes

    # example: ARC4_DYNAMIC_BYTES


# example: ARC4_STRUCT
class Todo(arc4.Struct):
    task: arc4.String
    completed: arc4.Bool


Todos: t.TypeAlias = arc4.DynamicArray[Todo]


class Arc4Struct(ARC4Contract):

    def __init__(self) -> None:
        self.todos = Todos()

    @abimethod()
    def add_todo(self, task: arc4.String) -> Todos:
        todo = Todo(task=task, completed=arc4.Bool(False))  # noqa: FBT003

        if not self.todos:
            self.todos = Todos(todo.copy())
        else:
            self.todos.append(todo.copy())

        return self.todos

    @abimethod()
    def complete_todo(self, task: arc4.String) -> None:

        for index in urange(self.todos.length):
            if self.todos[index].task == task:
                self.todos[index].completed = arc4.Bool(True)  # noqa: FBT003
                break

    @abimethod()
    def return_todo(self, task: arc4.String) -> Todo:
        todo_to_return: Todo

        exist = False
        for index in urange(self.todos.length):

            if self.todos[index].task == task:
                todo_to_return = self.todos[index].copy()
                exist = True

        assert exist

        return todo_to_return


# example: ARC4_STRUCT

# example: ARC4_TUPLE
contact_info_tuple = arc4.Tuple[
    arc4.String, arc4.String, arc4.UInt64
]  # name, email, phone


class Arc4Tuple(ARC4Contract):

    def __init__(self) -> None:
        self.contact_info = GlobalState(
            contact_info_tuple((arc4.String(""), arc4.String(""), arc4.UInt64(0)))
        )

    @abimethod()
    def add_contact_info(self, contact: contact_info_tuple) -> UInt64:
        """An arc4.Tuple is a heterogeneous collection of arc4 types."""
        name, email, phone = contact.native

        assert name.native == "Alice"
        assert email.native == "alice@something.com"
        assert phone == arc4.UInt64(555_555_555)

        self.contact_info.value = contact

        return phone.native

    @abimethod()
    def return_contact(self) -> arc4.Tuple[arc4.String, arc4.String, arc4.UInt64]:
        """An arc4.Tuple can be returned when more than one return value is needed."""

        return self.contact_info.value


# example: ARC4_TUPLE
