from algokit_utils import CommonAppCallParams, SendParams, config

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)
from smart_contracts.artifacts.reference_account.reference_account_client import (
    GetAccountBalanceWithArgumentArgs,
)


def account_reference_example_method1() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_account_app_client = env.reference_account_app_client

    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1
    # Configure automatic resource population per app call
    result1 = reference_account_app_client.send.get_account_balance(
        send_params=SendParams(populate_app_call_resources=True)
    )

    print("Method #1 Account Balance", result1.abi_return)

    # Or set the default value for populate_app_call_resources to true globally and apply to all app calls
    config.config.configure(populate_app_call_resources=True)

    result2 = reference_account_app_client.send.get_account_balance()

    print("Method #1 Account Balance", result2.abi_return)
    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1


def account_reference_example_method2() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_account_app_client = env.reference_account_app_client
    reference_account = env.reference_account

    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2
    # Include the account reference in the app call argument to be populated automatically
    result = reference_account_app_client.send.get_account_balance_with_argument(
        args=GetAccountBalanceWithArgumentArgs(account=reference_account.address)
    )

    print("Method #2 Account Balance", result.abi_return)
    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2


def account_reference_example_method3() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_account_app_client = env.reference_account_app_client
    reference_account = env.reference_account

    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3
    # Include the account reference in the account_references array to be populated manually
    result = reference_account_app_client.send.get_account_balance(
        params=CommonAppCallParams(account_references=[reference_account.address])
    )

    print("Method #3 Account Balance", result.abi_return)
    # example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3


if __name__ == "__main__":
    account_reference_example_method1()
    account_reference_example_method2()
    account_reference_example_method3()
