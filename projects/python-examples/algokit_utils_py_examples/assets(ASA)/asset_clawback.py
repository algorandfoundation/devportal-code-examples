from algokit_utils import AssetTransferParams

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def asset_clawback() -> None:

    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    manager = env.account_a  # Using account_a as the manager
    account_to_be_clawbacked = (
        env.account_b
    )  # Using account_b as the account to be clawed back

    # example: ASSET_CLAWBACK_TRANSACTION

    """
    An asset clawback transaction is an asset transfer transaction with the
    `clawback_target` set to the account that is being clawed back from.

    Parameters for an asset transfer transaction.
    - sender: The address of the account that will send the transaction
    - asset_id: ID of the asset
    - amount: Amount of the asset to transfer (smallest divisible unit)
    - receiver: The account to send the asset to
    - clawback_target: The account to take the asset from, defaults to None
    """

    txn_result = algorand_client.send.asset_transfer(
        AssetTransferParams(
            sender=manager.address,
            asset_id=1234,
            amount=1,
            receiver=manager.address,
            clawback_target=account_to_be_clawbacked.address,  # account that is being clawed back from
        )
    )

    # example: ASSET_CLAWBACK_TRANSACTION
