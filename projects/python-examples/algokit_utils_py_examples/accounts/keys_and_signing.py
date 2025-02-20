from algokit_utils import AlgoAmount, PaymentParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def keys_and_signing() -> None:
    # example: KEYS_AND_SIGNING

    algorand_client, _, account_a, account_b, _ = setup_localnet_environment()
    algorand_client._default_validity_window = 1000

    """
    Sets the default signer to use if no other signer is specified.
    If this isn't set and a transaction needs signing for a given sender then an error will be thrown from get_signer / get_account.
    """
    algorand_client.account.set_default_signer(account_a.signer)

    """
    Returns the TransactionSigner for the given sender address.
    If no signer has been registered for that address then the default signer is used if registered.
    """
    signer = algorand_client.account.get_signer(account_a.address)

    """
    account_a is a `SigningAccount` that already has a signer.
    Therefore you can just send transactions through the algorand client without manually signing.
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
        )
    )

    payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_b.address,
            receiver=account_a.address,
            amount=AlgoAmount(algo=1),
        )
    )

    """
    The unsigned transaction can be signed by the signer when sending with the `add_transaction` method.
    """
    algorand_client.new_group().add_transaction(
        transaction=payment_txn, signer=account_b.signer
    ).send()

    # example: KEYS_AND_SIGNING


keys_and_signing()
