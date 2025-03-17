# pyright: reportMissingModuleSource=false
from algopy import ARC4Contract, GlobalState, UInt64
from algopy.arc4 import abimethod


class CustomCreate(ARC4Contract):
    def __init__(self) -> None:
        self.age = GlobalState(UInt64)

    @abimethod(create="require")
    def custom_create(self, age: UInt64) -> None:
        self.age.value = age

    @abimethod()
    def get_age(self) -> UInt64:
        return self.age.value
