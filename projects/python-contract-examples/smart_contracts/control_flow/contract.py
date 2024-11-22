import typing as t

from algopy import ARC4Contract, String, UInt64, arc4, uenumerate, urange


# example: IF_ELSE
class IfElseExample(ARC4Contract):

    @arc4.abimethod
    def is_rich(self, account_balance: UInt64) -> String:
        if account_balance > 1000:
            return String("This account is rich!")
        elif account_balance > 100:
            return String("This account is doing well.")
        else:
            return String("This account is poor :(")

    @arc4.abimethod
    def is_even(self, number: UInt64) -> String:
        return String("Even") if number % 2 == 0 else String("Odd")


# example: IF_ELSE

# example: FOR_LOOP
FourArray: t.TypeAlias = arc4.StaticArray[arc4.UInt8, t.Literal[4]]


class ForLoopsExample(ARC4Contract):

    # urange: reversed items, forward index
    @arc4.abimethod
    def for_loop(self) -> FourArray:
        array = FourArray(arc4.UInt8(0), arc4.UInt8(0), arc4.UInt8(0), arc4.UInt8(0))

        for index, item in uenumerate(reversed(urange(4))):  # [3, 2, 1, 0]
            array[index] = arc4.UInt8(item)

        for index in urange(4):  # [0, 1, 2, 3]
            array[index] = arc4.UInt8(index)
        return array


# example: FOR_LOOP


# example: MATCH
class MatchStatements(ARC4Contract):

    @arc4.abimethod
    def get_day(self, date: UInt64) -> String:

        match date:
            case UInt64(1):
                return String("Monday")
            case UInt64(2):
                return String("Tuesday")
            case UInt64(3):
                return String("Wednesday")
            case UInt64(4):
                return String("Thursday")
            case UInt64(5):
                return String("Friday")
            case UInt64(6):
                return String("Saturday")
            case UInt64(7):
                return String("Sunday")
            case _:
                return String("Invalid day")


# example: MATCH


# example: WHILE_LOOP
class WhileLoopExample(ARC4Contract):

    @arc4.abimethod
    def clean_rooms(self) -> UInt64:

        # Clean all rooms except the closet
        robot_energy = UInt64(100)
        current_room = String("kitchen")

        while robot_energy > 0:
            if current_room == "closet":
                current_room = String("kitchen")
                continue

            if current_room == "kitchen":
                current_room = String("living room")
            elif current_room == "living room":
                current_room = String("closet")

            robot_energy -= 50

            if robot_energy == 0:
                break

        return robot_energy


# example: WHILE_LOOP
