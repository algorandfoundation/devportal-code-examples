from algokit_utils import AssetOptInParams, CommonAppCallParams, SendParams, config

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)
from smart_contracts.artifacts.reference_account_asset.reference_account_asset_client import (
    GetAssetBalanceWithArgArgs,
)


def account_asset_reference_example_method1() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_account = env.reference_account
    account_asset_reference_app_client = env.account_asset_reference_app_client
    reference_asset_id = env.reference_asset_id
    algorand_client = env.algorand_client

    # Opt into the asset
    algorand_client.send.asset_opt_in(
        AssetOptInParams(
            sender=reference_account.address,
            asset_id=reference_asset_id,
        )
    )

    # example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_1
    # Configure automatic resource population per app call
    result1 = account_asset_reference_app_client.send.get_asset_balance(
        send_params=SendParams(populate_app_call_resources=True)
    )

    print("Method #1 Asset Balance", result1.abi_return)

    # Or set the default value for populate_app_call_resources to true globally and apply to all app calls
    config.config.configure(populate_app_call_resources=True)

    result2 = account_asset_reference_app_client.send.get_asset_balance()

    print("Method #1 Asset Balance", result2.abi_return)
    # example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_1


def account_asset_reference_example_method2() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    account_asset_reference_app_client = env.account_asset_reference_app_client
    reference_asset_id = env.reference_asset_id

    # example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_2
    # Include the account and asset references in the app call arguments to be populated automatically
    result = account_asset_reference_app_client.send.get_asset_balance_with_arg(
        args=GetAssetBalanceWithArgArgs(
            acct="R3J76MDPEXQEWBV2LQ6FLQ4PYC4QXNHHPIL2BX2KSFU4WUNJJMDBTLRNEM",
            asset=reference_asset_id,
        )
    )

    print("Method #2 Asset Balance", result.abi_return)
    # example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_2


def account_asset_reference_example_method3() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    account_asset_reference_app_client = env.account_asset_reference_app_client
    reference_asset_id = env.reference_asset_id

    # example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_3
    # Manually provide both account and asset references in the respective arrays
    result = account_asset_reference_app_client.send.get_asset_balance(
        params=CommonAppCallParams(
            account_references=[
                "R3J76MDPEXQEWBV2LQ6FLQ4PYC4QXNHHPIL2BX2KSFU4WUNJJMDBTLRNEM"
            ],
            asset_references=[reference_asset_id],
        )
    )

    print("Method #3 Asset Balance", result.abi_return)
    # example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_3


if __name__ == "__main__":
    account_asset_reference_example_method1()
    account_asset_reference_example_method2()
    account_asset_reference_example_method3()
