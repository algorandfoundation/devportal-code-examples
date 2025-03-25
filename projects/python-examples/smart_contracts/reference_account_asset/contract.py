# example: REFERENCE_ACCOUNT_ASSET_EXAMPLE
from algopy import Account, ARC4Contract, Asset, UInt64
from algopy.arc4 import abimethod

"""
A contract that demonstrates how to reference both accounts and assets in a smart contract
"""


class ReferenceAccountAsset(ARC4Contract):
    """
    Returns the balance of a specific asset in a hardcoded account
    @returns The asset balance of the account
    """

    @abimethod
    def get_asset_balance(self) -> UInt64:
        acct = Account(
            "WMHF4FLJNKY2BPFK7YPV5ID6OZ7LVDB2B66ZTXEAMLL2NX4WJZRJFVX66M"
        )  # Replace with your account address
        asset = Asset(1185)  # Replace with your asset id

        assert acct.is_opted_in(asset), "Account is not opted in to the asset"

        return asset.balance(acct)

    """
    Returns the balance of a specific asset in a provided account
    @param account The account to check the asset balance for
    @param asset The asset to check the balance of
    @returns The asset balance of the account
    """

    @abimethod
    def get_asset_balance_with_arg(self, acct: Account, asset: Asset) -> UInt64:
        assert acct.is_opted_in(asset), "Account is not opted in to the asset"
        # Get the asset balance
        return asset.balance(acct)


# example: REFERENCE_ACCOUNT_ASSET_EXAMPLE
