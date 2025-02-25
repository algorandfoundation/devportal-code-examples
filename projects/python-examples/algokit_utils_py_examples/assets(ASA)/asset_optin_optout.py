from algokit_utils import AssetOptInParams, AssetOptOutParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def asset_optin_optout() -> None:

    algorand_client, _, account_a, account_b, _ = setup_localnet_environment()

    # example: ASSET_OPT_IN_TRANSACTION

    """
    Send an asset opt in transaction for account_a opting in to asset with asset id 1234

    Parameters for an asset opt in transaction.
    - sender: The address of the account that will opt in to the asset
    - asset_id: ID of the asset
    """
    txn_result = algorand_client.send.asset_opt_in(
        AssetOptInParams(
            sender=account_a.address,
            asset_id=1234,
        )
    )

    # example: ASSET_OPT_IN_TRANSACTION

    # example: ASSET_OPT_OUT_TRANSACTION

    """
    Send an asset opt out transaction for account_a opting out of asset with asset id 1234

    Parameters for an asset opt out transaction.
    - sender: The address of the account that will opt out of the asset
    - asset_id: ID of the asset
    - creator: The creator address of the asset
    - ensure_zero_balance: Check if account has zero balance before opt-out, defaults to True
    """
    txn_result = algorand_client.send.asset_opt_out(
        params=AssetOptOutParams(
            sender=account_a.address,
            asset_id=1234,
            creator=account_b.address,
        ),
        ensure_zero_balance=True,
    )

    # example: ASSET_OPT_OUT_TRANSACTION
