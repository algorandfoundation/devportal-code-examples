from algokit_utils import (
    AlgoAmount,
    CommonAppCallParams,
    PaymentParams,
    SendParams,
    config,
)

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)
from smart_contracts.artifacts.reference_app_box.reference_app_box_client import (
    IncrementBoxCounterArgs,
)


def app_box_reference_example_method1() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_a = env.account_a
    reference_app_box_app_client = env.reference_app_box_app_client

    # Get the box MBR amount from the contract
    box_mbr_response = reference_app_box_app_client.send.get_box_mbr()
    box_mbr: int = box_mbr_response.abi_return or 0

    counter_app_address = reference_app_box_app_client.app_address

    # Fund the contract account with enough Algos before proceeding
    algorand_client.send.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=counter_app_address,
            amount=AlgoAmount(algo=1),
            note=b"METHOD 1: Funding contract account",
        )
    )

    # example: APP_BOX_REFERENCE_EXAMPLE_METHOD_1
    # Create payment for MBR
    pay_mbr = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=counter_app_address,
            amount=AlgoAmount(micro_algo=box_mbr),
        )
    )

    # Method 1: Using populate_app_call_resources in send_params
    response1 = reference_app_box_app_client.send.increment_box_counter(
        args=IncrementBoxCounterArgs(pay_mbr=pay_mbr),
        params=CommonAppCallParams(sender=account_a.address),
        send_params=SendParams(populate_app_call_resources=True),
    )

    print("Method #1 Box Counter (explicit):", response1.abi_return)

    # Method 2: Configure globally
    # Set the default value for populate_app_call_resources to true once and apply to all contract invocations
    config.config.configure(populate_app_call_resources=True)

    # Create another payment for MBR
    pay_mbr2 = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=counter_app_address,
            amount=AlgoAmount(micro_algo=box_mbr),
        )
    )

    # With global configuration, we don't need to specify populate_app_call_resources
    response2 = reference_app_box_app_client.send.increment_box_counter(
        args=IncrementBoxCounterArgs(pay_mbr=pay_mbr2),
        params=CommonAppCallParams(sender=account_a.address),
    )

    print("Method #1 Box Counter (global):", response2.abi_return)
    # example: APP_BOX_REFERENCE_EXAMPLE_METHOD_1


def app_box_reference_example_method2() -> None:
    # Setup the test environment
    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_b = env.account_b
    reference_app_box_app_client = env.reference_app_box_app_client

    # Get the box MBR amount from the contract
    box_mbr_response = reference_app_box_app_client.send.get_box_mbr()
    box_mbr: int = box_mbr_response.abi_return or 0

    counter_app_address = reference_app_box_app_client.app_address

    # IMPORTANT: Fund the contract account with enough Algo before proceeding
    algorand_client.send.payment(
        PaymentParams(
            sender=account_b.address,
            receiver=counter_app_address,
            amount=AlgoAmount(algo=1),
            note=b"METHOD 2: Funding contract account",
        )
    )

    # example: APP_BOX_REFERENCE_EXAMPLE_METHOD_2
    box_prefix = b"counter"  # box identifier prefix
    public_key = account_b.public_key

    # Create the box reference
    box_reference = box_prefix + public_key

    # Create payment for MBR
    pay_mbr = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_b.address,
            receiver=counter_app_address,
            amount=AlgoAmount(micro_algo=box_mbr),
        )
    )

    # Call the smart contract with manually specified box reference
    response = reference_app_box_app_client.send.increment_box_counter(
        args=IncrementBoxCounterArgs(pay_mbr=pay_mbr),
        params=CommonAppCallParams(
            sender=account_b.address, box_references=[box_reference]
        ),
    )

    print("Method #2 Box Counter:", response.abi_return)
    # example: APP_BOX_REFERENCE_EXAMPLE_METHOD_2


if __name__ == "__main__":
    app_box_reference_example_method1()
    app_box_reference_example_method2()
