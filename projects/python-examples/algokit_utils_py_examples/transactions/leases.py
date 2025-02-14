from algokit_utils import AlgoAmount, PaymentParams, SendParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def leases() -> None:
    # example: LEASES

    algorand_client, _, account1, _, _ = setup_localnet_environment()

    # Create a lease value - this could be any unique string or Uint8Array
    lease: bytes = b"unique-lease-value"

    """
    Send a payment transaction with a lease
    If another transaction with the same lease and sender tries to execute within the validity window,
    it will be rejected
    """
    result = algorand_client.send.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account1.address,
            amount=AlgoAmount(algo=1),
            lease=lease,
            # Optional: Set a custom validity window for the lease
            validity_window=2,  # Number of rounds the lease is valid for
        )
    )

    """
    Attempting to send another transaction with the same lease and sender within the validity window
    will cause the transaction to be rejected
    """
    try:
        algorand_client.send.payment(
            PaymentParams(
                sender=account1.address,  # Same sender as first transaction
                receiver=account1.address,
                amount=AlgoAmount(algo=1),
                lease=lease,
            ),
            send_params=SendParams(
                suppress_log=True,
            ),
        )
    except Exception as e:
        print("Transaction rejected due to active lease")

    """
    Sending empty payment txn to progress the block round
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account1.address,
            amount=AlgoAmount(algo=0),
        )
    )

    """
    This payment transaction with the same lease and sender will be accepted
    because the first_valid_round is outside the validity window of the first transaction
    """
    pay_txn = algorand_client.send.payment(
        PaymentParams(
            sender=account1.address,  # Same sender as first transaction
            receiver=account1.address,
            amount=AlgoAmount(algo=1),
            lease=lease,
        )
    )


leases()
