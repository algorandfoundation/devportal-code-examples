from algokit_utils import AssetOptInParams, AssetOptOutParams

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def asset_optin_optout() -> None:
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_a = env.account_a
    account_b = env.account_b

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

    # example: ASSET_BULK_OPT_IN_TRANSACTION

    """
    Opt an account in to a list of Algorand Standard Assets.

    :param account: The account to opt-in
    :param asset_ids: The list of asset IDs to opt-in to
    :param signer: The signer to use for the transaction, defaults to None
    :param rekey_to: The address to rekey the account to, defaults to None
    :param note: The note to include in the transaction, defaults to None
    :param lease: The lease to include in the transaction, defaults to None
    :param static_fee: The static fee to include in the transaction, defaults to None
    :param extra_fee: The extra fee to include in the transaction, defaults to None
    :param max_fee: The maximum fee to include in the transaction, defaults to None
    :param validity_window: The validity window to include in the transaction, defaults to None
    :param first_valid_round: The first valid round to include in the transaction, defaults to None
    :param last_valid_round: The last valid round to include in the transaction, defaults to None
    :param send_params: The send parameters to use for the transaction, defaults to None
    :return: An array of records matching asset ID to transaction ID of the opt in
    """
    txn_results = algorand_client.asset.bulk_opt_in(
        account=account_a.address,
        asset_ids=[1234, 5678],
    )

    print(txn_results[0].transaction_id, txn_results[1].transaction_id)

    # example: ASSET_BULK_OPT_IN_TRANSACTION

    # example: ASSET_BULK_OPT_OUT_TRANSACTION

    """
    Opt an account out of a list of Algorand Standard Assets.

    :param account: The account to opt-out
    :param asset_ids: The list of asset IDs to opt-out of
    :param ensure_zero_balance: Whether to check if the account has a zero balance first, defaults to True
    :param signer: The signer to use for the transaction, defaults to None
    :param rekey_to: The address to rekey the account to, defaults to None
    :param note: The note to include in the transaction, defaults to None
    :param lease: The lease to include in the transaction, defaults to None
    :param static_fee: The static fee to include in the transaction, defaults to None
    :param extra_fee: The extra fee to include in the transaction, defaults to None
    :param max_fee: The maximum fee to include in the transaction, defaults to None
    :param validity_window: The validity window to include in the transaction, defaults to None
    :param first_valid_round: The first valid round to include in the transaction, defaults to None
    :param last_valid_round: The last valid round to include in the transaction, defaults to None
    :param send_params: The send parameters to use for the transaction, defaults to None
    :raises ValueError: If ensure_zero_balance is True and account has non-zero balance or is not opted in
    :return: An array of records matching asset ID to transaction ID of the opt out
    """
    txn_results = algorand_client.asset.bulk_opt_out(
        account=account_a.address,
        asset_ids=[1234, 5678],
    )

    print(txn_results[0].transaction_id, txn_results[1].transaction_id)

    # example: ASSET_BULK_OPT_OUT_TRANSACTION
