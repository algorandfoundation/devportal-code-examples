from algokit_utils import AlgoAmount, CommonAppCallParams, SendParams, config

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)
from smart_contracts.artifacts.reference_app.reference_app_client import (
    IncrementViaInnerWithArgArgs,
)


def app_reference_example_method1() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_app_client = env.reference_app_app_client

    # example: APP_REFERENCE_EXAMPLE_METHOD_1
    # Configure automatic resource population per app call
    result1 = reference_app_client.send.increment_via_inner(
        send_params=SendParams(populate_app_call_resources=True),
    )

    print("Method #1 Increment via inner:", result1.abi_return)

    # Or set the default value for populate_app_call_resources to true globally and apply to all app calls
    config.config.configure(
        populate_app_call_resources=True,
    )

    result2 = reference_app_client.send.increment_via_inner(
        params=CommonAppCallParams(
            extra_fee=AlgoAmount(micro_algo=1000)
        ),  # additional fee to cover the inner app call
    )

    print("Method #1 Increment via inner:", result2.abi_return)
    # example: APP_REFERENCE_EXAMPLE_METHOD_1


def app_reference_example_method2() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_app_client = env.reference_app_app_client

    # example: APP_REFERENCE_EXAMPLE_METHOD_2
    # Include the app reference in the app call argument to be populated automatically
    result = reference_app_client.send.increment_via_inner_with_arg(
        args=IncrementViaInnerWithArgArgs(app=1717),
        params=CommonAppCallParams(
            extra_fee=AlgoAmount(micro_algo=1000)
        ),  # additional fee to cover the inner app call
    )

    print("Method #2 Increment via inner:", result.abi_return)
    # example: APP_REFERENCE_EXAMPLE_METHOD_2


def app_reference_example_method3() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    reference_app_client = env.reference_app_app_client

    # example: APP_REFERENCE_EXAMPLE_METHOD_3
    # Include the app reference in the app_references array to be populated
    result = reference_app_client.send.increment_via_inner(
        params=CommonAppCallParams(
            app_references=[1717],
            extra_fee=AlgoAmount(
                micro_algo=1000
            ),  # additional fee to cover the inner app call
        ),
    )

    print("Method #3 Increment via inner:", result.abi_return)
    # example: APP_REFERENCE_EXAMPLE_METHOD_3


if __name__ == "__main__":
    app_reference_example_method1()
    app_reference_example_method2()
    app_reference_example_method3()
