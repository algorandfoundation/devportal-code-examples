from algokit_utils import AssetDestroyParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def asset_delete() -> None:

    algorand_client, _, account_a, _, _ = setup_localnet_environment()

    # example: ASSET_DESTROY_TRANSACTION
    """
    Send an asset destroy transaction destroying an asset with asset id 1234
    All of the assets must be owned by the creator of the asset before the asset can be deleted.

    Parameters for destroying an asset.
    - sender: The address of the account that will send the transaction
    - asset_id: ID of the asset
    """
    txn_result = algorand_client.send.asset_destroy(
        AssetDestroyParams(
            sender=account_a.address,
            asset_id=1234,
        )
    )

    # example: ASSET_DESTROY_TRANSACTION
