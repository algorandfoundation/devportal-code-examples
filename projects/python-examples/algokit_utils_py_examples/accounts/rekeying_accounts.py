from algokit_utils import AlgoAmount, AlgorandClient, PaymentParams, SendParams


def rekeying_accounts() -> None:
    # example: REKEYING_ACCOUNT

    """
    Initialize an Algorand client instance configured for LocalNet
    """
    algorand_client = AlgorandClient.default_localnet()

    """
    Create random accounts that can be used for testing or development.
    Each account will have a newly generated private/public key pair.
    """
    account1 = algorand_client.account.random()
    account2 = algorand_client.account.random()

    """
    Returns the default LocalNet dispenser account.
    This account can be used to fund test accounts on LocalNet.
    """
    localnet_dispenser = algorand_client.account.localnet_dispenser()

    algorand_client.account.ensure_funded(
        account1, localnet_dispenser, AlgoAmount(algo=10)
    )

    """
    Rekey an account to use a different address for signing.
    This allows account 1 to be controlled by account 2's private key.
    """
    algorand_client.account.rekey_account(account=account1, rekey_to=account2)

    payment_txn_result = algorand_client.send.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account2.address,
            amount=AlgoAmount(algo=1),
        )
    )

    unsigned_payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account2.address,
            amount=AlgoAmount(algo=1),
        )
    )

    """
    The unsigned transaction can be signed by the signer when sending with the `add_transaction` method.
    """
    # TODO: Fix this. how can I pass in params?
    algorand_client.new_group().add_transaction(
        transaction=unsigned_payment_txn, signer=account2.signer
    ).send()

    # example: REKEYING_ACCOUNT


rekeying_accounts()
