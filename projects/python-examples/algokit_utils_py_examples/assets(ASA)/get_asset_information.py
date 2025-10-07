from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def get_asset_information() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client

    # example: GET_ASSET_INFORMATION

    """Get information about an Algorand Standard Asset (ASA).

    - asset_id: The ID of the asset
    - creator: The address of the account that created the asset
    - total: The total amount of the smallest divisible units that were created of the asset
    - decimals: The amount of decimal places the asset was created with
    - default_frozen: Whether the asset was frozen by default for all accounts, defaults to None
    - manager: The address of the optional account that can manage the configuration of the asset and destroy it,
        defaults to None
    - reserve: The address of the optional account that holds the reserve (uncirculated supply) units of the asset,
        defaults to None
    - freeze: The address of the optional account that can be used to freeze or unfreeze holdings of this asset,
        defaults to None
    - clawback: The address of the optional account that can clawback holdings of this asset from any account,
        defaults to None
    - unit_name: The optional name of the unit of this asset (e.g. ticker name), defaults to None
    - unit_name_b64: The optional name of the unit of this asset as bytes, defaults to None
    - asset_name: The optional name of the asset, defaults to None
    - asset_name_b64: The optional name of the asset as bytes, defaults to None
    - url: Optional URL where more information about the asset can be retrieved, defaults to None
    - url_b64: Optional URL where more information about the asset can be retrieved as bytes, defaults to None
    - metadata_hash: 32-byte hash of some metadata that is relevant to the asset and/or asset holders,
        defaults to None
    """
    asset_info = algorand_client.asset.get_by_id(1234)

    print(asset_info.asset_name)
    print(asset_info.total)

    # example: GET_ASSET_INFORMATION
