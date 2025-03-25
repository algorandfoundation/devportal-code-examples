from algokit_utils import AssetFreezeParams

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def asset_freeze() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_a = env.account_a
    account_b = env.account_b

    # example: ASSET_FREEZE_TRANSACTION

    """
    Send an asset freeze transaction freezing an asset with asset id 1234

    Parameters for freezing an asset.
    - sender: The address of the account that will send the transaction
    - asset_id: The ID of the asset
    - account: The account to freeze or unfreeze
    - frozen: Whether the assets in the account should be frozen
    """
    txn_result = algorand_client.send.asset_freeze(
        AssetFreezeParams(
            sender=account_a.address,
            asset_id=1234,
            account=account_b.address,  # The account to freeze or unfreeze
            frozen=True,
        )
    )

    """
    Send an asset unfreeze transaction unfreezing an asset with asset id 1234
    """
    txn_result = algorand_client.send.asset_freeze(
        AssetFreezeParams(
            sender=account_a.address,
            asset_id=1234,
            account=account_b.address,  # The account to freeze or unfreeze
            frozen=False,
        )
    )

    # example: ASSET_FREEZE_TRANSACTION
