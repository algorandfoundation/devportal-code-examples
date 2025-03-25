from algokit_utils import AssetTransferParams

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def asset_transfer() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_a = env.account_a
    account_b = env.account_b

    # example: ASSET_TRANSFER_TRANSACTION

    """
    Send an asset transfer transaction of 1 asset with asset id 1234 from account_a to account_b

    Parameters for an asset transfer transaction.
    - sender: The address of the account that will send the asset
    - asset_id: The asset id of the asset to transfer
    - amount: Amount of the asset to transfer (smallest divisible unit)
    - receiver: The address of the account to send the asset to
    """
    txn_result = algorand_client.send.asset_transfer(
        AssetTransferParams(
            sender=account_a.address,
            asset_id=1234,
            receiver=account_b.address,
            amount=1,
        )
    )

    # example: ASSET_TRANSFER_TRANSACTION
