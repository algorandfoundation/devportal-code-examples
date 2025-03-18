from algokit_utils import AlgoAmount, PaymentParams

from algokit_utils_py_examples.helpers import setup_localnet_environment


def rekeying_accounts() -> None:

    algorand_client, _, account_a, account_b, account_c = setup_localnet_environment()

    # example: REKEY_ACCOUNT
    """
    Rekey an account to use a different address for signing.
    This allows account A to be controlled by account B's private key.
    """
    algorand_client.account.rekey_account(account=account_a.address, rekey_to=account_b)

    # Send a payment transaction from account A
    # which will automatically sign the transaction with account B's private key
    payment_txn_result = algorand_client.send.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_c.address,
            amount=AlgoAmount(algo=1),
        )
    )

    unsigned_payment_txn = algorand_client.create_transaction.payment(
        PaymentParams(
            sender=account_a.address,
            receiver=account_c.address,
            amount=AlgoAmount(algo=1),
        )
    )

    """
    The unsigned transaction can be signed by the signer when sending with the `add_transaction` method.
    """
    result = (
        algorand_client.new_group()
        .add_transaction(transaction=unsigned_payment_txn, signer=account_b.signer)
        .send()
    )

    print(result.tx_ids)
    # example: REKEY_ACCOUNT


rekeying_accounts()
