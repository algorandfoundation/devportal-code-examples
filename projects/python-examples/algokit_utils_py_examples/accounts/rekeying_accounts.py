from algokit_utils import *


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

    txn1 = algorand_client.send.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account2.address,
            amount=AlgoAmount(algo=1),
        )
    )

    payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account1.address,
            receiver=account2.address,
            amount=AlgoAmount(algo=2),
        )
    )
    print(f"payment_txn: {payment_txn.get_txid()}")
    """
    The unsigned transaction can be signed by the signer when sending with the `add_transaction` method.
    """
    algorand_client.new_group().add_transaction(
        transaction=payment_txn, signer=account2.signer
    ).send()

    # example: REKEYING_ACCOUNT


rekeying_accounts()
