from algokit_utils import AssetConfigParams

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def asset_update() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_a = env.account_a
    account_b = env.account_b

    # example: ASSET_UPDATE_TRANSACTION

    """
    Send an asset config transaction updating four mutable fields of an asset:
    manager, reserve, freeze, clawback. This operation is only possible if the sender is
    the asset manager and the asset has all four mutable fields set.

    Parameters for configuring an existing asset.
    - sender: The address of the account that will send the transaction
    - asset_id: ID of the asset
    - manager: The address that can change the manager, reserve, clawback, and freeze addresses, defaults to None
    - reserve: The address that holds the uncirculated supply, defaults to None
    - freeze: The address that can freeze the asset in any account, defaults to None
    - clawback: The address that can clawback the asset from any account, defaults to None
    """
    txn_result = algorand_client.send.asset_config(
        AssetConfigParams(
            sender=account_a.address,
            asset_id=1234,
            manager=account_b.address,
            reserve=account_b.address,
            freeze=account_b.address,
            clawback=account_b.address,
        )
    )

    # example: ASSET_UPDATE_TRANSACTION
