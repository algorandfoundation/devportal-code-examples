from algokit_utils import AlgoAmount, PaymentParams

from algokit_utils_py_examples.helpers import (
    LocalnetEnvironment,
    setup_localnet_environment,
)


def keys_and_signing() -> None:
    # example: KEYS_AND_SIGNING

    env: LocalnetEnvironment = setup_localnet_environment()
    algorand_client = env.algorand_client
    account_a = env.account_a
    account_b = env.account_b
    account_c = env.account_c

    algorand_client._default_validity_window = 1000

    # example: DEFAULT_SIGNER
    """
    Sets the default signer to use if no other signer is specified.
    If this isn't set and a transaction needs signing for a given sender then an error
    will be thrown from get_signer / get_account.
    """
    algorand_client.account.set_default_signer(account_a.signer)

    # example: DEFAULT_SIGNER

    # example: MULTIPLE_SIGNERS
    """
    Register multiple transaction signers at once.
    Demonstrates the fluent interface for registering signers.
    """
    algorand_client.account.set_signer_from_account(account_a)
    algorand_client.account.set_signer_from_account(account_b)
    algorand_client.account.set_signer_from_account(account_c)

    # example: MULTIPLE_SIGNERS

    # example: GET_SIGNER
    """
    Returns the TransactionSigner for the given sender address.
    If no signer has been registered for that address then the default signer is used if registered.
    """
    signer = algorand_client.account.get_signer(account_a.address)

    # example: GET_SIGNER

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

    # example: OVERRIDE_SIGNER
    account_a_signer = algorand_client.account.get_signer(account_b.address)

    """
    Create an unsigned payment transaction and manually sign it.
    """
    payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_b.address,
            amount=AlgoAmount(algo=1),
            note=b"Payment from A to B",
        )
    )

    """
    The transaction signer can be overridden in the second argument to `add_transaction`
    """
    algorand_client.new_group().add_transaction(
        transaction=payment_txn, signer=account_a_signer
    ).send()

    # example: OVERRIDE_SIGNER


keys_and_signing()
