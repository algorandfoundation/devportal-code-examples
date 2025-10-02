from algokit_utils import CommonAppCallParams, SendParams, config

from algokit_utils_py_examples.helpers import setup_localnet_environment
from smart_contracts.artifacts.reference_account_app.reference_account_app_client import (
    GetMyCounterWithArgArgs,
)


def account_app_reference_example_method1() -> None:
    # Setup the test environment
    env = setup_localnet_environment()
    reference_account_app_app_client = env.reference_account_app_app_client

    # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_1
    # Configure automatic resource population per app call
    result1 = reference_account_app_app_client.send.get_my_counter(
        send_params=SendParams(populate_app_call_resources=True)
    )

    print("Method #1 My Counter", result1.abi_return)

    # Or set the default value for populate_app_call_resources to true globally and apply to all app calls
    config.config.configure(populate_app_call_resources=True)

    result2 = reference_account_app_app_client.send.get_my_counter()

    print("Method #1 My Counter", result2.abi_return)
    # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_1


def account_app_reference_example_method2() -> None:
    # Setup the test environment
    env = setup_localnet_environment()
    reference_account_app_app_client = env.reference_account_app_app_client
    account_a = env.account_a

    # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_2
    # Include the account and app references in the app call arguments to be populated automatically
    result = reference_account_app_app_client.send.get_my_counter_with_arg(
        args=GetMyCounterWithArgArgs(
            acct=account_a.address,
            app=1717,  # Using the default app ID from the contract
        )
    )

    print("Method #2 My Counter", result.abi_return)
    # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_2


def account_app_reference_example_method3() -> None:
    # Setup the test environment
    env = setup_localnet_environment()
    reference_account_app_app_client = env.reference_account_app_app_client
    account_a = env.account_a

    # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_3
    # Manually provide both account and app references in the respective arrays
    result = reference_account_app_app_client.send.get_my_counter(
        CommonAppCallParams(
            account_references=[account_a.address],
            app_references=[1717],  # Using the default app ID from the contract
        )
    )

    print("Method #3 My Counter", result.abi_return)
    # example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_3


if __name__ == "__main__":
    # account_app_reference_example_method1()
    account_app_reference_example_method2()
    # account_app_reference_example_method3()
