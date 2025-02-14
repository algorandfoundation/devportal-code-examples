from algokit_utils import *
from algokit_utils_py_examples.helpers import setup_localnet_environment


def leases() -> None:
    # example: LEASES

    algorand_client, dispenser, account1, _, _ = setup_localnet_environment()
    print(f"Default validity window: {algorand_client._default_validity_window}")
    algorand_client.client.algod.set_timestamp_offset(0)

    offset = algorand_client.client.algod.get_timestamp_offset()
    print(f"Offset: {offset}")

    algod_response = algorand_client.client.algod.status()
    print(f"Algod response: {algod_response}")
    # Create a lease value - this could be any unique string or Uint8Array
    lease: bytes = b"unique-lease-value"

    # Send a payment transaction with a lease
    # If another transaction with the same lease and sender tries to execute within the validity window,
    # it will be rejected
    result = algorand_client.send.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account1.address,
            amount=AlgoAmount(algo=1),
            lease=lease,
            # Optional: Set a custom validity window for the lease
            validity_window=100,  # Number of rounds the lease is valid for
        )
    )

    # Attempting to send another transaction with the same lease and sender within the validity window
    # will cause the transaction to be rejected
    try:
        algorand_client.send.payment(
            PaymentParams(
                sender=account1.address,  # Same sender as first transaction
                receiver=account1.address,
                amount=AlgoAmount(algo=10),
                lease=lease,
            ),
            send_params=SendParams(
                suppress_log=True,
            ),
        )
    except Exception as e:
        print("Transaction rejected due to active lease")

    algorand_client.client.algod.set_timestamp_offset(101)
    offset = algorand_client.client.algod.get_timestamp_offset()
    print(f"Offset2: {offset}")

    algod_response = algorand_client.client.algod.status()
    print(f"Algod response2: {algod_response}")
    """
    This payment transaction with the same lease and sender will be accepted
    because the first_valid_round is set to the last_valid_round + 1 which is
    outside the validity window of the first transaction
    """
    # algorand_client.send.payment(
    #     PaymentParams(
    #         sender=account1.address,  # Same sender as first transaction
    #         receiver=account1.address,
    #         amount=AlgoAmount(algo=10),
    #         lease=lease,
    #     )
    # )


leases()
