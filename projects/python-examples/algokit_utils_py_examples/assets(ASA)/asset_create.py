from algokit_utils import AssetCreateParams

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def asset_create() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_a = env.account_a

    # example: ASSET_CREATE_TRANSACTION

    """
    Send an asset create transaction creating a fungible ASA with 10 million units

    Parameters for creating a new asset.
    - sender: The address of the account that will send the transaction
    - total: The total amount of the smallest divisible unit to create
    - decimals: The amount of decimal places the asset should have, defaults to None
    - default_frozen: Whether the asset is frozen by default in the creator address, defaults to None
    - manager: The address that can change the manager, reserve, clawback, and freeze addresses, defaults to None
    - reserve: The address that holds the uncirculated supply, defaults to None
    - freeze: The address that can freeze the asset in any account, defaults to None
    - clawback: The address that can clawback the asset from any account, defaults to None
    - unit_name: The short ticker name for the asset, defaults to None
    - asset_name: The full name of the asset, defaults to None
    """
    txn_result = algorand_client.send.asset_create(
        AssetCreateParams(
            sender=account_a.address,
            total=10_000_000,
            decimals=6,
            default_frozen=False,  # optional
            manager=account_a.address,  # optional. Can be permanently disabled by setting to None
            reserve=account_a.address,  # optional. Can be permanently disabled by setting to None
            freeze=account_a.address,  # optional. Can be permanently disabled by setting to None
            clawback=account_a.address,  # optional. Can be permanently disabled by setting to None
            unit_name="MYA",
            asset_name="My Asset",
        )
    )

    """
    Send an asset create transaction creating a 1 to 1 unique NFT
    """
    txn_result = algorand_client.send.asset_create(
        AssetCreateParams(
            sender=account_a.address,
            total=1,
            asset_name="My NFT",
            unit_name="MNFT",
            decimals=0,
            url="metadata URL",
            metadata_hash=b"Hash of the metadata URL",
        )
    )
    # example: ASSET_CREATE_TRANSACTION
