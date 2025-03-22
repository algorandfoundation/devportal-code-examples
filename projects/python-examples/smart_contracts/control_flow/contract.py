import typing as t

from algopy import ARC4Contract, String, UInt64, arc4, uenumerate, urange


class IfElseExample(ARC4Contract):
    # example: IF_ELSE
    @arc4.abimethod
    def is_rich(self, account_balance: UInt64) -> String:
        if account_balance > 1000:
            return String("This account is rich!")
        elif account_balance > 100:
            return String("This account is doing well.")
        else:
            return String("This account is poor :(")

    # example: IF_ELSE

    # example: TERNARY
    @arc4.abimethod
    def is_even(self, number: UInt64) -> String:
        return String("Even") if number % 2 == 0 else String("Odd")

    # example: TERNARY


# example: FOR_LOOP
FourArray: t.TypeAlias = arc4.StaticArray[arc4.UInt8, t.Literal[4]]


class ForLoopsExample(ARC4Contract):
    # urange: reversed items, forward index
    @arc4.abimethod
    def for_loop(self) -> FourArray:
        array = FourArray(arc4.UInt8(0), arc4.UInt8(0), arc4.UInt8(0), arc4.UInt8(0))

        for index, item in uenumerate(reversed(urange(4))):  # [3, 2, 1, 0]
            array[index] = arc4.UInt8(item)

        x = UInt64(0)

        for item in urange(1, 5):  # [1, 2, 3, 4]
            x += item

        assert x == 10

        return array


# example: FOR_LOOP


# example: MATCH
class MatchStatements(ARC4Contract):
    @arc4.abimethod
    def get_day(self, date: UInt64) -> String:
        match date:
            case UInt64(0):
                return String("Monday")
            case UInt64(1):
                return String("Tuesday")
            case UInt64(2):
                return String("Wednesday")
            case UInt64(3):
                return String("Thursday")
            case UInt64(4):
                return String("Friday")
            case UInt64(5):
                return String("Saturday")
            case UInt64(6):
                return String("Sunday")
            case _:
                return String("Invalid day")


# example: MATCH


# example: WHILE_LOOP
class WhileLoopExample(ARC4Contract):
    @arc4.abimethod
    def loop(self) -> UInt64:
        num = UInt64(10)
        loop_count = UInt64(0)

        while num > 0:
            if num > 5:
                num -= 1
                loop_count += 1
                continue

            num -= 2
            loop_count += 1

            if num == 1:
                break

        return loop_count


# example: WHILE_LOOP
