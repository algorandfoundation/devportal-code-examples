from algokit_utils import CommonAppCallParams, SendParams, config

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)
from smart_contracts.artifacts.reference_asset.reference_asset_client import (
    GetAssetTotalSupplyWithArgArgs,
)


def asset_reference_example_method1() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_asset_client = env.reference_asset_app_client

    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1
    # Configure automatic resource population per app call
    result1 = reference_asset_client.send.get_asset_total_supply(
        send_params=SendParams(populate_app_call_resources=True),
    )

    print("Method #1 Asset Total Supply:", result1.abi_return)

    # Or set the default value for populate_app_call_resources to true globally and apply to all app calls
    config.config.configure(
        populate_app_call_resources=True,
    )

    result2 = reference_asset_client.send.get_asset_total_supply()

    print("Method #1 Asset Total Supply:", result2.abi_return)
    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1


def asset_reference_example_method2() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_asset_client = env.reference_asset_app_client
    reference_asset_id = env.reference_asset_id

    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2
    # Include the account reference in the app call argument to be populated automatically
    result = reference_asset_client.send.get_asset_total_supply_with_arg(
        args=GetAssetTotalSupplyWithArgArgs(asset=reference_asset_id),
    )

    print("Method #2 Asset Total Supply:", result.abi_return)
    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2


def asset_reference_example_method3() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_asset_client = env.reference_asset_app_client
    reference_asset_id = env.reference_asset_id

    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3
    # Include the asset reference in the asset_references array to be populated
    result = reference_asset_client.send.get_asset_total_supply(
        params=CommonAppCallParams(asset_references=[reference_asset_id]),
    )

    print("Method #3 Asset Total Supply:", result.abi_return)
    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3


if __name__ == "__main__":
    asset_reference_example_method1()
    asset_reference_example_method2()
    asset_reference_example_method3()
