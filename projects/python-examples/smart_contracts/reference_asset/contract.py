# example: GET_ASSET_REFERENCE_EXAMPLE

from algopy import ARC4Contract, Asset, UInt64
from algopy.arc4 import abimethod

"""
A contract that demonstrates how to use resource usage in a contract using an asset reference
"""


class ReferenceAsset(ARC4Contract):
    """
    Returns the total supply of the asset
    @returns The total supply of the asset
    """

    @abimethod
    def get_asset_total_supply(self) -> UInt64:
        return Asset(1185).total  # Replace with your asset id

    """
    Returns the total supply of the asset
    @param asset The asset to get the total supply of
    @returns The total supply of the asset
    """

    @abimethod
    def get_asset_total_supply_with_arg(self, asset: Asset) -> UInt64:
        return asset.total


# example: GET_ASSET_REFERENCE_EXAMPLE
