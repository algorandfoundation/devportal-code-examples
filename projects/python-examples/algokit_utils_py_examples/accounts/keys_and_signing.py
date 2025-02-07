from algokit_utils import AlgoAmount, AlgorandClient, PaymentParams


def keys_and_signing() -> None:
    # example: KEYS_AND_SIGNING

    """
    Initialize an Algorand client instance configured for LocalNet
    """
    algorand_client = AlgorandClient.default_localnet()
    algorand_client._default_validity_window = 1000

    """
    Create 3 random accounts
    """
    random_account1 = algorand_client.account.random()
    random_account2 = algorand_client.account.random()
    dispenser = algorand_client.account.localnet_dispenser()

    algorand_client.account.ensure_funded(
        random_account1, dispenser, AlgoAmount(algo=10)
    )
    algorand_client.account.ensure_funded(
        random_account2, dispenser, AlgoAmount(algo=10)
    )

    """
    Sets the default signer to use if no other signer is specified.
    If this isn't set and a transaction needs signing for a given sender then an error will be thrown from get_signer / get_account.
    """
    algorand_client.account.set_default_signer(random_account1.signer)

    """
    Returns the TransactionSigner for the given sender address.
    If no signer has been registered for that address then the default signer is used if registered.
    """
    signer = algorand_client.account.get_signer(random_account1.address)

    """
    random_account1 is a `SigningAccount` that already has a signer.
    Therefore you can just send transactions through the algorand client without manually signing.
    """
    algorand_client.send.payment(
        PaymentParams(
            sender=random_account1.address,
            receiver=random_account2.address,
            amount=AlgoAmount(algo=1),
        )
    )

    payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=random_account2.address,
            receiver=random_account1.address,
            amount=AlgoAmount(algo=1),
        )
    )

    """
    The unsigned transaction can be signed by the signer when sending with the `add_transaction` method.
    """
    algorand_client.new_group().add_transaction(
        transaction=payment_txn, signer=random_account2.signer
    ).send()

    # example: KEYS_AND_SIGNING


keys_and_signing()
