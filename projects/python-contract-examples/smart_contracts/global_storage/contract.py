from algopy import (
    Account,
    Application,
    ARC4Contract,
    Asset,
    Bytes,
    GlobalState,
    UInt64,
    arc4,
)


class GlobalStorage(ARC4Contract):
    # example: INIT_GLOBAL_STORAGE
    def __init__(self) -> None:
        self.global_int_full = GlobalState(UInt64(50))  # UInt64 with default value = 50
        self.global_int_simplified = UInt64(
            10
        )  # UInt64 simplified with default value = 10
        self.global_int_no_default = GlobalState(UInt64)  # UInt64 with no default value

        # example: INIT_BYTES
        self.global_bytes_full = GlobalState(
            Bytes(b"Hello")
        )  # Bytes with default value = bytes(Hello)
        self.global_bytes_simplified = Bytes(
            b"Hello"
        )  # Bytes simplified with default value = bytes(Hello)
        self.global_bytes_no_default = GlobalState(Bytes)  # Bytes with no default value
        # example: INIT_BYTES

        self.global_bool_simplified = True  # Bool
        self.global_bool_no_default = GlobalState(bool)  # Bool

        self.global_asset = GlobalState(Asset)  # Asset
        self.global_application = GlobalState(Application)  # Application
        self.global_account = GlobalState(Account)  # Account

    # example: INIT_GLOBAL_STORAGE

    # example: READ_GLOBAL_STATE
    @arc4.abimethod
    def get_global_state(self) -> UInt64:
        return self.global_int_full.get(default=UInt64(0))

    @arc4.abimethod
    def maybe_global_state(self) -> tuple[UInt64, bool]:
        int_value, int_exists = self.global_int_full.maybe()  # uint64
        if not int_exists:
            int_value = UInt64(0)
        return int_value, int_exists

    @arc4.abimethod
    def get_global_state_example(self) -> bool:
        assert self.global_int_full.get(default=UInt64(0)) == 50  # uint64
        assert self.global_int_simplified == UInt64(10)  # get function cannot be used
        assert self.global_int_no_default.get(default=UInt64(0)) == 0

        assert self.global_bytes_full.get(Bytes(b"default")) == b"Hello"  # byte
        return True

    # example: READ_GLOBAL_STATE

    # example: READ_GLOBAL_STATE_EXAMPLES
    @arc4.abimethod
    def maybe_global_state_example(self) -> bool:
        int_value, i_exists = self.global_int_full.maybe()  # uint64
        assert i_exists
        assert int_value == UInt64(50)

        byte_value, b_exists = self.global_bytes_full.maybe()  # byte
        assert b_exists
        assert byte_value == b"Hello"

        byte_del_value, b_exists = self.global_bytes_full.maybe()
        assert not b_exists
        assert self.global_bytes_full.value == Bytes(b"Hello")

        bool_value, i_exists = self.global_bool_no_default.maybe()  # bool
        assert i_exists
        assert bool(bool_value)

        asset_value, i_exists = self.global_asset.maybe()  # Asset
        assert i_exists
        assert asset_value == Asset(UInt64(10))

        appln_value, i_exists = self.global_application.maybe()  # Application
        assert i_exists
        assert appln_value == Application(UInt64(10))

        return True

    # example: READ_GLOBAL_STATE_EXAMPLES

    # example: VALUE_PROPERTY_GLOBAL_STATE_EXAMPLES
    @arc4.abimethod
    def check_global_state_example(self) -> bool:
        assert self.global_int_full.value == 50  # uint64
        assert self.global_bytes_full.value == Bytes(b"Hello")  # byte

        assert self.global_int_simplified == 10  # uint64
        assert self.global_bytes_simplified == b"Hello"  # byte
        assert bool(self.global_bool_simplified)

        assert not self.global_int_no_default
        assert not self.global_bytes_no_default
        assert not self.global_bool_no_default

        assert self.global_asset.value == Asset(UInt64(10))  # Asset
        assert self.global_application.value == Application(UInt64(10))  # Application
        assert self.global_account.value == Account(Bytes(b"Hello"))  # Account
        return True

    # example: VALUE_PROPERTY_GLOBAL_STATE_EXAMPLES

    # example: WRITE_GLOBAL_STATE
    @arc4.abimethod
    def set_global_state(self, value: Bytes) -> None:
        self.global_bytes_full.value = value

    # example: WRITE_GLOBAL_STATE

    # example: WRITE_GLOBAL_STATE_EXAMPLES
    @arc4.abimethod
    def set_global_state_example(
        self,
        value_bytes: Bytes,
        value_asset: Asset,
        *,
        value_bool: bool,
    ) -> None:
        self.global_bytes_no_default.value = value_bytes
        assert self.global_bytes_no_default.value == value_bytes

        self.global_bool_no_default.value = value_bool  # Bool
        assert bool(self.global_bool_no_default.value)

        self.global_asset.value = value_asset  # Asset
        assert self.global_asset.value == value_asset

    # example: WRITE_GLOBAL_STATE_EXAMPLES

    # example: DELETE_GLOBAL_STATE
    @arc4.abimethod
    def del_global_state(self) -> bool:
        del self.global_int_full.value
        return True

    # example: DELETE_GLOBAL_STATE

    # example: DELETE_GLOBAL_STATE_EXAMPLES
    @arc4.abimethod
    def del_global_state_example(self) -> bool:
        del self.global_bytes_no_default.value
        del self.global_bool_no_default.value
        del self.global_asset.value
        return True

    # example: DELETE_GLOBAL_STATE_EXAMPLES
