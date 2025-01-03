from algopy import (
    Account,
    Application,
    ARC4Contract,
    Asset,
    Bytes,
    LocalState,
    UInt64,
    arc4,
)


# example: LOCAL_STORAGE
class LocalStorage(ARC4Contract):
    def __init__(self) -> None:
        ## Initialise local storages
        self.local_int = LocalState(UInt64)  # Uint64
        self.local_bytes = LocalState(Bytes)  # Bytes
        self.local_bool = LocalState(bool)  # Bool
        self.local_asset = LocalState(Asset)  # Asset
        self.local_application = LocalState(Application)  # Application
        self.local_account = LocalState(Account)  # Account

    @arc4.abimethod
    def contains_local_data(self, for_account: Account) -> bool:
        assert for_account in self.local_int  # Uint64
        return True

    @arc4.abimethod
    def contains_local_data_example(self, for_account: Account) -> bool:
        assert for_account in self.local_int  # Uint64
        assert for_account in self.local_bytes  # Bytes
        assert for_account in self.local_bool  # Bool
        assert for_account in self.local_asset  # Asset
        assert for_account in self.local_application  # Application
        assert for_account in self.local_account  # Account
        return True

    # delete local data
    @arc4.abimethod
    def delete_local_data(self, for_account: Account) -> None:
        del self.local_account[for_account]  # Uint64

    @arc4.abimethod
    def delete_local_data_example(self, for_account: Account) -> bool:
        del self.local_int[for_account]  # Uint64
        del self.local_bytes[for_account]  # Bytes
        del self.local_bool[for_account]  # Bool
        del self.local_asset[for_account]  # Asset
        del self.local_application[for_account]  # Application
        del self.local_account[for_account]  # Account
        return True

    # get item
    @arc4.abimethod
    def get_item_local_data(self, for_account: Account) -> UInt64:
        return self.local_int[for_account]

    @arc4.abimethod
    def get_item_local_data_example(self, for_account: Account) -> bool:
        assert self.local_int[for_account] == UInt64(
            10
        )  # Uint64 - returns guranteed data
        assert self.local_bytes[for_account] == b"Hello"  # Bytes
        assert bool(self.local_bool[for_account])  # Bool
        assert self.local_asset[for_account] == Asset(UInt64(10))  # Asset
        assert self.local_application[for_account] == Application(
            UInt64(10)
        )  # Application
        assert self.local_account[for_account] == Account(Bytes(b"Hello"))  # Account
        return True

    # set item
    @arc4.abimethod
    def set_local_int(self, for_account: Account, value: UInt64) -> None:
        self.local_int[for_account] = value  # Uint64

    @arc4.abimethod
    def set_local_data_example(
        self,
        for_account: Account,
        value_asset: Asset,
        value_account: Account,
        value_appln: Application,
        value_byte: Bytes,
        *,
        value_bool: bool,
    ) -> bool:
        self.local_bytes[for_account] = value_byte  # Bytes
        assert self.local_bytes[for_account] == value_byte

        self.local_bool[for_account] = value_bool  # Bool
        assert self.local_bool[for_account] == value_bool

        self.local_asset[for_account] = value_asset  # Asset
        assert self.local_asset[for_account] == value_asset

        self.local_application[for_account] = value_appln  # Application
        assert self.local_application[for_account] == value_appln

        self.local_account[for_account] = value_account  # Account
        assert self.local_account[for_account] == value_account
        return True

    # get function
    @arc4.abimethod
    def get_local_data_with_default_int(self, for_account: Account) -> UInt64:
        return self.local_int.get(for_account, default=UInt64(0))  # Uint64

    @arc4.abimethod
    def get_local_data_with_default(self, for_account: Account) -> bool:
        assert self.local_int.get(for_account, default=UInt64(0)) == UInt64(
            10
        )  # Uint64
        assert self.local_bytes.get(
            for_account, default=Bytes(b"Default Value")
        ) == Bytes(
            b"Hello"
        )  # Bytes
        assert bool(self.local_bool.get(for_account, default=False))  # Bool

        assert self.local_asset.get(for_account, default=Asset(UInt64(0))) == Asset(
            UInt64(10)
        )  # Asset
        assert self.local_application.get(
            for_account, default=Application(UInt64(0))
        ) == Application(
            UInt64(10)
        )  # Application
        assert self.local_account.get(
            for_account, default=Account(Bytes(b"Default Value"))
        ) == Account(
            Bytes(b"Hello")
        )  # Account

        return True

    # maybe function
    @arc4.abimethod
    def maybe_local_data(self, for_account: Account) -> tuple[UInt64, bool]:
        # used to get data or assert int
        result, exists = self.local_int.maybe(for_account)  # Uint64
        if not exists:
            result = UInt64(0)
        return result, exists

    @arc4.abimethod
    def maybe_local_data_example(self, for_account: Account) -> bool:
        result, exists = self.local_int.maybe(for_account)  # Uint64
        assert exists, "no data for account"
        assert result == UInt64(10)

        result_bytes, exists = self.local_bytes.maybe(for_account)  # Bytes
        assert exists, "no data for account"
        assert result_bytes == b"Hello"

        result_bool, exists = self.local_bool.maybe(for_account)  # Bool
        assert exists, "no data for account"
        assert bool(result_bool)

        result_asset, exists = self.local_asset.maybe(for_account)  # Asset
        assert exists, "no data for account"
        assert result_asset == Asset(UInt64(10))

        result_appln, exists = self.local_application.maybe(for_account)  # Application
        assert exists, "no data for account"
        assert result_appln == Application(UInt64(10))

        result_account, exists = self.local_account.maybe(for_account)  # Account
        assert exists, "no data for account"
        assert result_account == Account(Bytes(b"Hello"))
        return True
